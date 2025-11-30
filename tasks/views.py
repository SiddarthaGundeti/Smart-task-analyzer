from rest_framework.decorators import api_view


@api_view(['POST'])
def analyze_tasks(request):
"""Accepts a JSON array of tasks and returns them with scores sorted descending."""
tasks = request.data
if not isinstance(tasks, list):
return Response({'error': 'Expected a list of tasks'}, status=400)


# detect circular dependencies
cycles = detect_circular_dependencies(tasks)


results = []
for t in tasks:
# basic validation via serializer
serializer = TaskSerializer(data=t)
if not serializer.is_valid():
# include errors but continue
t['_errors'] = serializer.errors
score = calculate_task_score(t, all_tasks=tasks)
t['score'] = score
results.append(t)


results = sorted(results, key=lambda x: x.get('score', 0), reverse=True)


output = {'cycles': cycles, 'results': results}
return Response(output)




@api_view(['GET'])
def suggest_tasks(request):
"""Return top 3 tasks from query param 'tasks' (JSON encoded list) or from DB (optional)."""
tasks_param = request.query_params.get('tasks')
tasks = None
if tasks_param:
try:
tasks = json.loads(tasks_param)
except Exception:
return Response({'error': 'Invalid JSON in tasks parameter'}, status=400)
else:
return Response({'error': 'Provide tasks param'}, status=400)


for t in tasks:
t['score'] = calculate_task_score(t, all_tasks=tasks)


sorted_tasks = sorted(tasks, key=lambda x: x.get('score', 0), reverse=True)
top3 = sorted_tasks[:3]


# build explanations
for task in top3:
why = []
due = task.get('due_date')
try:
due_date = date.fromisoformat(due)
days_left = (due_date - date.today()).days
if days_left < 0:
why.append('Overdue')
elif days_left <= 3:
why.append('Due soon')
except Exception:
pass
if task.get('estimated_hours', 1) < 2:
why.append('Quick win')
if task.get('importance', 5) >= 7:
why.append('High importance')
task['why'] = '; '.join(why) or 'Balanced priority'


return Response({'top': top3})
