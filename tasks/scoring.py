from datetime import date, timedelta
dfs(node, [node])


return cycles




def calculate_task_score(task, all_tasks=None, config=ScoringConfig):
"""
Calculate a numeric score for a task dict. Higher -> higher priority.
task: dict with keys title, due_date, estimated_hours, importance, dependencies
all_tasks: optional list of tasks to analyze dependencies
"""
score = 0
today = date.today()


due = parse_date(task.get('due_date'))
if due is None:
# invalid or missing date: treat as low urgency but not zero
# return a minimal score but allow importance to matter
due_days = None
else:
due_days = (due - today).days


# Urgency
if due_days is None:
score += 0
else:
if due_days < 0:
score += config.URGENT_OVERDUE
elif due_days <= 3:
score += config.URGENT_SOON
else:
# small linear urgency for longer dates
score += max(0, (30 - due_days) // 3)


# Importance
importance = task.get('importance')
try:
importance = int(importance)
except Exception:
importance = 5
score += importance * config.IMPORTANCE_WEIGHT


# Effort (favor quick wins)
est = task.get('estimated_hours')
try:
est = int(est)
except Exception:
est = 1
if est <= 0:
est = 1
if est < 2:
score += config.QUICK_WIN_BONUS
else:
# penalize very large tasks slightly
score += max(0, 5 - min(4, est // 4))


# Dependencies: if this task blocks others, increase priority
deps = task.get('dependencies', []) or []
if deps:
# if it blocks others (i.e., others depend on it), add more
blocking_count = 0
if all_tasks:
tid = task.get('id')
for t in all_tasks:
if tid in (t.get('dependencies') or []):
blocking_count += 1
score += config.DEPENDENCY_WEIGHT + blocking_count * 5


return score
