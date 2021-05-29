from datetime import datetime
from sqlalchemy import nullslast
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import TaskForm, CompletedForm, DeleteForm
from app.models import Task

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    taskform = TaskForm()
    if taskform.validate_on_submit():
        task = Task(task=taskform.task.data, deadline=taskform.deadline.data)
        db.session.add(task)
        db.session.commit()
        flash('Task added')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    tasks = Task.query.filter_by(completed=False).order_by(nullslast(Task.deadline.asc())).paginate(page, app.config['TASKS_PER_PAGE'], False)
    compforms = {}
    delforms = {}
    for t in tasks.items:
        compforms[t.id] = CompletedForm()
        delforms[t.id] = DeleteForm()
    for t_id, form in compforms.items():
        if form.complete.data and form.validate_on_submit():
            task = Task.query.filter_by(id=t_id).first()
            task.completed = not task.completed
            db.session.add(task)
            db.session.commit()
            flash('Task completed!')
            return redirect(url_for('index'))
    for t_id, form in delforms.items():
        if form.delete.data and form.validate_on_submit():
            task = Task.query.filter_by(id=t_id).first()
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted!')
            return redirect(url_for('index'))
    
    next_url = url_for('index', page=tasks.next_num) \
        if tasks.has_next else None
    prev_url = url_for('index', page=tasks.prev_num) \
        if tasks.has_prev else None

    return render_template('index.html', title='Tasks', taskform=taskform, compforms=compforms,
                           delforms=delforms, tasks=tasks.items, next_url=next_url, prev_url=prev_url)


@app.route('/completed', methods=['GET', 'POST'])
def completed():
    page = request.args.get('page', 1, type=int)
    tasks = Task.query.filter_by(completed=True).paginate(page, app.config['TASKS_PER_PAGE'], False)
    compforms = {}
    delforms = {}
    for t in tasks.items:
        compforms[t.id] = CompletedForm()
        delforms[t.id] = DeleteForm()
    for t_id, form in compforms.items():
        if form.validate_on_submit():
            task = Task.query.filter_by(id=t_id).first()
            task.completed = not task.completed
            db.session.add(task)
            db.session.commit()
            flash('Task removed from completed!')
            return redirect(url_for('completed'))
    for t_id, form in delforms.items():
        if form.delete.data and form.validate_on_submit():
            task = Task.query.filter_by(id=t_id).first()
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted!')
            return redirect(url_for('index'))
    
    next_url = url_for('completed', page=tasks.next_num) \
        if tasks.has_next else None
    prev_url = url_for('completed', page=tasks.prev_num) \
        if tasks.has_prev else None

    return render_template('index.html', title='Completed Tasks', compforms=compforms,
                           delforms=delforms, tasks=tasks.items, next_url=next_url, prev_url=prev_url)