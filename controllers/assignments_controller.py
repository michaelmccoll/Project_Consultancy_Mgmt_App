from flask import Flask, render_template, request, redirect
from flask import Blueprint
from repositories import consultant_repository, client_repository, assignment_repository
from models.assignment import Assignment

assignments_blueprint = Blueprint("assignments",__name__)

@assignments_blueprint.route('/assignments')
def assignments():
    assignments = assignment_repository.select_all()
    return render_template("assignments/index.html", all_assignments=assignments)

@assignments_blueprint.route("/assignments/new")
def new_assignment():
    consultants = consultant_repository.select_all()
    clients = client_repository.select_all()
    return render_template("assignments/new.html", all_consultants=consultants, all_clients=clients)

@assignments_blueprint.route("/assignments", methods=['POST'])
def create_assignment():
    description = request.form["description"]
    consultant_id = request.form["consultant_id"]
    consultant = consultant_repository.select(consultant_id)
    client_id = request.form["client_id"]
    client = client_repository.select(client_id)
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    days_required = request.form["days_required"]
    calculate_costs = Assignment.calculate_costs(consultant.day_rate,days_required)
    new_assignment = Assignment(description,consultant,client,days_required,start_date,end_date, calculate_costs)
    assignment_repository.save(new_assignment)
    return redirect("/assignments")

@assignments_blueprint.route("/assignments/<id>")
def show_assignment(id):
    assignment = assignment_repository.select(id)
    clients = client_repository.clients(assignment)
    consultants = consultant_repository.consultants(assignment)
    return render_template("assignments/show.html",assignment=assignment,clients=clients,consultants=consultants)

@assignments_blueprint.route("/assignments/<id>", methods=['POST'])
def update_assignment(id):
    description = request.form["description"]
    consultant_id = request.form["consultant_id"]
    consultant = consultant_repository.select(consultant_id)
    client_id = request.form["client_id"]
    client = client_repository.select(client_id)
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    days_required = request.form["days_required"]
    calculate_costs = Assignment.calculate_costs(consultant.day_rate,days_required)
    assignment = Assignment(description,consultant,client,days_required,start_date,end_date,calculate_costs,id)
    assignment_repository.update(assignment)
    return redirect("/assignments")

@assignments_blueprint.route("/assignments/<id>/edit", methods=['GET'])
def edit_assignment(id):
    assignment = assignment_repository.select(id)
    clients = client_repository.select_all()
    consultants = consultant_repository.select_all()
    return render_template("/assignments/edit.html", assignment=assignment,clients=clients,consultants=consultants)

@assignments_blueprint.route("/assignments/<id>/delete", methods=['POST'])
def delete_assignment(id):
    assignment_repository.delete(id)
    return redirect ("/assignments")