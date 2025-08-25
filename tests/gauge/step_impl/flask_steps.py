import requests
import time
from getgauge.python import step, after_spec
from results_collector import record_result, save_results


def timed_request(name, method, url, **kwargs):
    """Выполнить HTTP-запрос с измерением времени и выводом результатов"""
    start = time.perf_counter()
    resp = requests.request(method, url, **kwargs)
    elapsed = time.perf_counter() - start
    record_result("Flask", name, elapsed, resp.status_code)
    print(f"{name} | {method.upper()} | {url} | {elapsed:.3f}s | {resp.status_code}")
    return resp


@step("Run full CRUD scenario for Flask API <table>")
def run(table):
    if not table.rows:
        raise ValueError("Таблица пустая! Убедитесь, что в спецификации есть хотя бы один URL.")
    
    base_url = table.rows[0][0]
    task_id = None

    try:
        # --- СОЗДАНИЕ ---
        resp = timed_request("Create task", "post", base_url, json={"title": "test", "description": "demo"})
        assert resp.status_code == 201
        task = resp.json()
        task_id = str(task["id"])

        # --- СОЗДАНИЕ (ошибка: отсутствует title) ---
        resp_bad = timed_request("Create without title", "post", base_url, json={"description": "no title"})
        assert resp_bad.status_code == 400

        # --- СПИСОК ---
        resp_list = timed_request("List tasks", "get", base_url)
        assert resp_list.status_code == 200
        assert any(t["id"] == task_id for t in resp_list.json())

        # --- ПОЛУЧЕНИЕ ПО ID (успешно) ---
        resp_get = timed_request("Get by id", "get", f"{base_url}{task_id}/")
        assert resp_get.status_code == 200

        # --- ПОЛУЧЕНИЕ НЕСУЩЕСТВУЮЩЕЙ ЗАДАЧИ ---
        resp_get_404 = timed_request("Get non-existent task", "get",
                                     f"{base_url}00000000-0000-0000-0000-000000000000/")
        assert resp_get_404.status_code == 404

        # --- ОБНОВЛЕНИЕ ---
        resp_update = timed_request("Update task", "put", f"{base_url}{task_id}/",
                                    json={"title": "updated", "status": "завершено"})
        assert resp_update.status_code == 200

        # --- ОБНОВЛЕНИЕ ПУСТЫМ ТЕЛОМ ---
        resp_update_empty = timed_request("Update with empty body", "put", f"{base_url}{task_id}/", json={})
        assert resp_update_empty.status_code == 422

        # --- МЕТОД НЕ РАЗРЕШЕН ---
        assert timed_request("PUT on list", "put", base_url, json={}).status_code == 405
        assert timed_request("POST on detail", "post", f"{base_url}{task_id}/", json={}).status_code == 405

        # --- УДАЛЕНИЕ ---
        assert timed_request("Delete task", "delete", f"{base_url}{task_id}/").status_code == 204

        # --- УДАЛЕНИЕ СНОВА ---
        assert timed_request("Delete already removed", "delete", f"{base_url}{task_id}/").status_code == 404

        # --- ПОЛУЧЕНИЕ ПОСЛЕ УДАЛЕНИЯ ---
        assert timed_request("Get after deletion", "get", f"{base_url}{task_id}/").status_code == 404

    finally:
        if task_id:
            # --- ОЧИСТКА ---
            timed_request("Cleanup", "delete", f"{base_url}{task_id}/")


@after_spec
def finalize_spec(spec):
    save_results()
