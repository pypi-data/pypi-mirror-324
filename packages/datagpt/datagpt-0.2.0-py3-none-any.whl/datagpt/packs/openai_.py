import openai
from openai import pagination

import os
from dataclasses import dataclass, field


@dataclass
class ResultBase:
    status: bool = 0
    reason_status_0: str = ""

@dataclass
class Results(ResultBase):
    raw_results: list[pagination.SyncCursorPage] | None = field(default_factory=list)

@dataclass
class IdNameListResults(Results):
    names: list[str] = field(default_factory=list)
    ids: list[str] = field(default_factory=list)
    dict_name_id: dict = field(default_factory=dict)

@dataclass
class Result(ResultBase):
    raw_result: pagination.SyncCursorPage | None = None

@dataclass
class IdNameListResult(Result):
    names: list[str] = field(default_factory=list)
    ids: list[str] = field(default_factory=list)
    dict_name_id: dict = field(default_factory=dict)


class Storage:
    def __init__(self, api_key: str):
        try:
            self.client = openai.OpenAI(api_key=api_key)
            # Тестируем подключение, вызывая любой безопасный метод
            self.client.models.list()
        except openai.PermissionDeniedError as e:
            raise RuntimeError(
                "Ошибка доступа к OpenAI API: страна или регион не поддерживается. "
                "Попробуйте использовать VPN."
            ) from e
        except openai.OpenAIError as e:
            raise RuntimeError(
                "Ошибка при подключении к OpenAI API. Проверьте API-ключ и интернет-соединение."
            ) from e


    def get_uploaded_file_list(self) -> IdNameListResults:
        ret = IdNameListResults()
        ret.raw_result = self.client.files.list()
        for n in ret.raw_result.data:
            ret.names.append(n.filename)
            ret.ids.append(n.id)
            ret.dict_name_id[n.filename] = n.id
        ret.status = 1
        return ret
    

    def get_vector_store_list(self) -> IdNameListResults:
        ret = IdNameListResults()
        ret.raw_result = self.client.beta.vector_stores.list()
        for n in ret.raw_result.data:
            ret.names.append(n.name)
            ret.ids.append(n.id)
            ret.dict_name_id[n.name] = n.id
        ret.status = 1
        return ret


    def get_vector_store_uploaded_file_list(self, vs_name: str):
        ret = IdNameListResults()
        dict_vs_name_id = self.get_vector_store_list().dict_name_id[vs_name]
        ret.raw_result = self.client.beta.vector_stores.files.list(dict_vs_name_id)
 
        ret.status = 1
        return ret


    def add_files_to_vector_store(self, file_paths: list[str], vs_name: str):
        ret = IdNameListResults()
        for n in file_paths:
            if os.path.isfile(n):
                continue
            else:
                ret.reason_status_0 = f"'{n}' - файл не существует на локальном"
                return ret
        gvsl = self.get_vector_store_list()
        vector_store_id = None
        if vs_name in gvsl.names:
            vector_store_id = gvsl.dict_name_id[vs_name]
        else:
            r = self.client.beta.vector_stores.create(name=vs_name)
            ret.raw_results.append(r)
            vector_store_id = r.id

        gufl = self.get_uploaded_file_list()
        for n in file_paths:
            f = os.path.basename(n)
            if f in gufl.names:
                ret.reason_status_0 = f"'{n}' - файл существует в облаке, а дубликат файлов не должен был, иначе удалить"
                return ret
            else:
                continue
        file_ids = []
        for n in file_paths:
            with open(n, "rb") as file:
                r = self.client.files.create(file=file, purpose="assistants")
                ret.raw_results.append(r)
                
            file_ids.append(r.id)
        self.client.beta.vector_stores.file_batches.create(
            vector_store_id=vector_store_id,
            file_ids=file_ids
            )
        ret.status = 1
        return ret


    def delete_files_from_vector_store(self, filenames:list[str], vs_name: str):
        ret = IdNameListResults()
        gufl = self.get_uploaded_file_list()
        for n_file in filenames:
            # if n in gufl.filenames:
            #     continue
            # else:
            #     ret.reason_status_0 = f"{n} - не существует в облаке"
            #     return ret
            try:
                index = gufl.names.index(n_file)  # Проверяем, есть ли файл
            except ValueError:
                ret.reason_status_0 = f"'{n_file}' - файл не существует в облаке"
                return ret

        gvsl = self.get_vector_store_list()
        try:
            index = gvsl.names.index(vs_name)  # Проверяем, есть ли файл
        except ValueError:
            ret.reason_status_0 = f"'{n_file}' векторное хранилище - не существует в облаке"
            return ret
            

        for n_file in filenames:
            r1 = self.client.files.delete(file_id=gufl.dict_name_id[n_file])
            ret.raw_results.append(r1)
            r2 = self.client.beta.vector_stores.files.delete(
                vector_store_id=gvsl.dict_name_id[vs_name],
                file_id=gufl.dict_name_id[n_file]
            )
            ret.raw_results.append(r2)
        ret.status = 1
        return ret


class Assistant:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.thread = None


    def set_id(self, id):
        self.set_id = id


    def new_chat_and_run(self, prompt=None):
        self.thread = self.client.beta.threads.create(
                messages=[
                {
                "role": "user",
                "content": prompt,
                }
            ]
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id, assistant_id=self.set_id
        )
        
        messages = list(self.client.beta.threads.messages.list(thread_id=self.thread.id, run_id=run.id))
        if not messages:
            raise RuntimeError("Ошибка: OpenAI не вернул сообщений в ответ.")
        
        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        for annotation in annotations:
            message_content.value = message_content.value.replace(annotation.text, "")
        return message_content.value