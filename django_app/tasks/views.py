# tasks/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task


@csrf_exempt
def task_list(request):
    if request.method == 'GET':
        tasks = [t.to_dict() for t in Task.objects.all()]
        return JsonResponse(tasks, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            task = Task.objects.create(
                title=data['title'],
                description=data.get('description', ''),
                status=data.get('status', Task.Status.CREATED)
            )
            return JsonResponse(task.to_dict(), status=201)
        except KeyError:
            return JsonResponse({"error": "title is required"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    if request.method == 'GET':
        return JsonResponse(task.to_dict())

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body or '{}')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Проверяем, что в теле есть хотя бы одно поле для обновления
        if not any(key in data for key in ("title", "description", "status")):
            return JsonResponse({"error": "No fields to update"}, status=422)

        # Обновляем только переданные поля
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.save()
        return JsonResponse(task.to_dict())

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({}, status=204)

    return JsonResponse({"error": "Method not allowed"}, status=405)

