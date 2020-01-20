import os
import random
import requests

from flask import Flask, render_template, request, redirect, session, flash, abort
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_session import Session
from datetime import datetime
from ai.classes import *
from ai.helper import transformData
from bll.dataservice import get_data, insert_data, get_data_by_id, delete_data, save, update_data, req1, req2, req3, req4
from dal import db
from dal.db import db_string
from dal.dto import UserSkillDTO, ProfessionSkillDTO
from dal.model import Person, Skill, UserSkill, Profession, ProfessionSkill, Vacancy
from forms.skill_form import SkillForm
from forms.user_form import UserForm
from forms.user_has_skill_form import UserSkillForm
from forms.profession_form import ProfessionForm
from forms.profession_has_skill_form import ProfessionSkillForm
from forms.vacancy_form import VacancyForm
from forms.real_form import SearchForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@app.route('/user', methods=['GET', 'POST'])
def user():
    result = get_data(Person)
    form = UserForm(request.form)
    if request.method == 'POST':
        print(form.id.data)

        if(form.id.data == ''):
            user = Person(int(random.getrandbits(31)), first_name = form.first_name.data, second_name = form.second_name.data, birthday = form.birthday.data, city = form.city.data)
            insert_data(user)
        else:
            user = Person(id = int(form.id.data), first_name = form.first_name.data, second_name = form.second_name.data, birthday = form.birthday.data, city = form.city.data)
            update_data(user, Person)
        save()
        return redirect('/user')

    return render_template('users.html', users = result, form = form)

@app.route('/user/delete/<id>')
def user_delete(id):
    delete_data(Person, id)
    save()
    return redirect('/user')

@app.route('/user/edit/<id>', methods=['GET'])
def user_edit(id):
    if request.method == 'GET':
        user = get_data_by_id(Person, id)
        result = get_data(Person)
        form = UserForm()
        form.id.data = user.id
        form.first_name.data = user.first_name
        form.second_name.data = user.second_name
        form.birthday.data = user.birthday
        form.city.data = user.city
        return render_template('users.html', users = result, form = form)


@app.route('/skill', methods=['GET', 'POST'])
def skill():
    result = get_data(Skill)
    form = SkillForm(request.form)
    if request.method == 'POST':
        print(form.id.data)
        ''''''
        if(form.id.data == ''):
            skill = Skill(int(random.getrandbits(31)), form.name.data)
            insert_data(skill)
        else:
            skill = Skill(int(form.id.data), form.name.data)
            update_data(skill, Skill)
        save()
        return redirect('/skill')

    return render_template('skill.html', skills = result, form = form)

@app.route('/skill/delete/<id>')
def skill_delete(id):
    delete_data(Skill, id)
    save()
    return redirect('/skill')

@app.route('/skill/edit/<id>', methods=['GET'])
def skill_edit(id):
    if request.method == 'GET':
        skill = get_data_by_id(Skill, id)
        result = get_data(Skill)
        form = SkillForm()
        form.id.data = skill.id
        form.name.data = skill.name
        return render_template('skill.html', skills = result, form = form)

@app.route('/userskill', methods=['GET', 'POST'])
def userskill():
    users = get_data(Person)
    skills = get_data(Skill)
    req = req2(Person, UserSkill, Skill)
    userskills = [UserSkillDTO(i[0], i[1] + ' ' + i[2], i[3]) for i in req]
    form = UserSkillForm(request.form)
    form.skill_id.choices = [(skill.id, skill.name) for skill in skills]
    form.user_id.choices = [(user.id, user.first_name) for user in users]
    if request.method == 'POST':
        print(form.id.data)

        if form.id.data == '':
            userskill = UserSkill(int(random.getrandbits(31)), form.user_id.data, form.skill_id.data)
            insert_data(userskill)
        else:
            userskill = UserSkill(int(form.id.data), form.user_id.data, form.skill_id.data)
            update_data(userskill, UserSkill)
        save()
        return redirect('/userskill')

    return render_template('user_has_skill.html', userskills = userskills, form = form)

@app.route('/userskill/delete/<id>')
def userskill_delete(id):
    delete_data(UserSkill, id)
    save()
    return redirect('/userskill')

@app.route('/userskill/edit/<id>', methods=['GET'])
def userskill_edit(id):
    if request.method == 'GET':
        userskill = get_data_by_id(UserSkill, id)

        users = get_data(Person)
        skills = get_data(Skill)
        req = req2(Person, UserSkill, Skill)
        userskills = [UserSkillDTO(i[0], i[1] + ' ' + i[2], i[3]) for i in req]

        form = UserSkillForm(request.form)
        form.skill_id.choices = [(skill.id, skill.name) for skill in skills]
        form.user_id.choices = [(user.id, user.first_name) for user in users]
        form.id.data = userskill.id
        form.skill_id.data = userskill.skill_id
        form.user_id.data = userskill.user_id
        return render_template('user_has_skill.html', userskills = userskills, form = form)


@app.route('/dashboard')
def dashboard():
    res1 = req1(Person, UserSkill, Skill)
    res2 = req3(Person, UserSkill, Skill)
    values1 = [i[1] for i in res1]
    labels1 = [i[0] for i in res1]
    values2 = [i[1] for i in res2]
    labels2 = [i[0] for i in res2]

    return render_template('dashboard.html', val1 = values1, lab1 = labels1, val2 = values2, lab2 = labels2)


@app.route('/profession', methods=['GET', 'POST'])
def profession():
    result = get_data(Profession)
    form = ProfessionForm(request.form)
    if request.method == 'POST':
        print(form.id.data)

        if(form.id.data == ''):
            print(form.name.data)
            profession = Profession(int(random.getrandbits(31)), name=form.name.data, minimal_work_expirience = int(form.minimal_work_expirience.data), minimal_education = form.minimal_education.data, category = form.category.data)
            insert_data(profession)
        else:
            profession = Profession(id=int(form.id.data),  name = form.name.data, minimal_work_expirience = form.minimal_work_expirience.data, minimal_education = form.minimal_education.data, category = form.category.data)
            update_data(profession, Profession)
        save()
        return redirect('/profession')

    return render_template('profession.html', professions = result, form = form)


@app.route('/profession/delete/<id>')
def profession_delete(id):
    delete_data(Profession, id)
    save()
    return redirect('/profession')


@app.route('/profession/edit/<id>', methods=['GET'])
def profession_edit(id):
    if request.method == 'GET':
        profession = get_data_by_id(Profession, id)
        result = get_data(Profession)
        form = ProfessionForm()
        form.id.data = profession.id
        form.name.data = profession.name
        form.minimal_work_expirience.data = profession.minimal_work_expirience
        form.minimal_education.data = profession.minimal_education
        form.category.data = profession.category
        return render_template('profession.html', professions = result, form = form)


@app.route('/vacancy', methods=['GET', 'POST'])
def vacancy():
    result = get_data(Vacancy)
    form = VacancyForm(request.form)
    professions = get_data(Profession)
    form.profession_id.choices = [(profession.id, profession.name) for profession in professions]

    if request.method == 'POST':
        print(form.id.data)

        if(form.id.data == ''):
            vacancy = Vacancy(int(random.getrandbits(31)), name = form.name.data, duties = form.duties.data, salary = form.salary.data, created_at=datetime.now(), description=form.description.data, profession_id = form.profession_id.data)
            insert_data(vacancy)
        else:
            vacancy = Vacancy(id = int(form.id.data), name = form.name.data, duties = form.duties.data, salary = form.salary.data, created_at=datetime.now(), description=form.description.data, profession_id = form.profession_id.data)
            update_data(vacancy, Vacancy)
        save()
        return redirect('/vacancy')

    return render_template('vacancy.html', vacancies = result, form = form)

@app.route('/vacancy/delete/<id>')
def vacancy_delete(id):
    delete_data(Vacancy, id)
    save()
    return redirect('/vacancy')

@app.route('/vacancy/edit/<id>', methods=['GET'])
def vacancy_edit(id):
    if request.method == 'GET':
        vacancy = get_data_by_id(Vacancy, id)
        professions = get_data(Profession)
        result = get_data(Vacancy)
        form = VacancyForm()
        form.id.data = vacancy.id
        form.name.data = vacancy.name
        form.description.data = vacancy.description
        form.duties.data = vacancy.duties
        form.salary.data = vacancy.salary
        form.profession_id.data = vacancy.profession_id
        form.profession_id.choices = [(profession.id, profession.name) for profession in professions]

        return render_template('vacancy.html', vacancies = result, form = form)


@app.route('/profession_skill', methods=['GET', 'POST'])
def profession_skill():
    professions = get_data(Profession)
    skills = get_data(Skill)
    req = req4(Profession, ProfessionSkill, Skill)
    professionskills = [ProfessionSkillDTO(i[0], i[1], i[2]) for i in req]
    form = ProfessionSkillForm(request.form)
    form.skill_id.choices = [(skill.id, skill.name) for skill in skills]
    form.profession_id.choices = [(profession.id, profession.name) for profession in professions]
    if request.method == 'POST':
        if form.id.data == '':
            professionskill = ProfessionSkill(int(random.getrandbits(31)), form.profession_id.data, form.skill_id.data)
            insert_data(professionskill)
        else:
            professionskill = ProfessionSkill(int(form.id.data), form.profession_id.data, form.skill_id.data)
            update_data(professionskill, ProfessionSkill)
        save()
        return redirect('/profession_skill')

    return render_template('profession_has_skill.html', professionskills = professionskills, form = form)

@app.route('/profession_skill/delete/<id>')
def profession_skill_delete(id):
    delete_data(ProfessionSkill, id)
    save()
    return redirect('/profession_skill')

@app.route('/profession_skill/edit/<id>', methods=['GET'])
def profession_skill_edit(id):
    if request.method == 'GET':
        professionskill = get_data_by_id(ProfessionSkill, id)

        professions = get_data(Profession)
        skills = get_data(Skill)
        req = req4(Profession, ProfessionSkill, Skill)
        professionskills = [ProfessionSkillDTO(i[0], i[1], i[2]) for i in req]

        form = ProfessionSkillForm(request.form)
        form.skill_id.choices = [(skill.id, skill.name) for skill in skills]
        form.profession_id.choices = [(profession.id, profession.name) for profession in professions]
        form.id.data = professionskill.id
        form.skill_id.data = professionskill.skill_id
        form.profession_id.data = professionskill.profession_id
        return render_template('profession_has_skill.html', professionskills = professionskills, form = form)


@app.route('/classification', methods=['GET'])
def classification():
    vacancies = get_data(Vacancy)
    vacanciesWithCategory = classificate_vacancy_by_salary(vacancies)
    return render_template('statistics.html', vacancies = vacanciesWithCategory)


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/real', methods=['GET', 'POST'])
def real():
    form = SearchForm(request.form)
    if request.method == 'POST':
        input = form.search.data
        url = 'https://rabota.ua/zapros/'+input+'/%d0%ba%d0%b8%d0%b5%d0%b2'
        output = requests.get(url).text
        etap_2 = transformData(output)
        if etap_2.__contains__('.f-404'):
            return render_template('real_vac.html', form=form,  vacancies='not found')
        else:
            return render_template('real_vac.html', form=form,  vacancies=etap_2)
    return render_template('real_vac.html', form=form,  vacancies='')

#if __name__ == '__main__':
#    manager.run()