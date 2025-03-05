from flask_login import login_required, current_user, login_user, logout_user
from flask import Flask, render_template, redirect, url_for, jsonify, url_for, flash, abort, request
from extensions import db, migrate, login_manager
from models import User, Event  
from forms import LoginForm, RegistrationForm, EventForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eventhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.options(db.joinedload(Event.organizer)).get_or_404(event_id)
    return render_template('event_detail.html', event=event)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            location=form.location.data,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('create_event.html', title='Create Event', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/event/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id) if event_id else None
    form = EventForm(obj=event)
    
    if form.validate_on_submit():
        if event:
            form.populate_obj(event)
            flash('Your event has been updated!', 'success')
        else:
            event = Event(user_id=current_user.id)
            form.populate_obj(event)
            db.session.add(event)
            flash('Your new event has been created!', 'success')
        
        db.session.commit()
        return redirect(url_for('event_detail', event_id=event.id))
    
    return render_template('edit_event.html', form=form, event=event)

@app.route('/event/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organizer != current_user:
        abort(403)  # Forbidden
    
    db.session.delete(event)
    db.session.commit()
    flash('Event has been deleted.', 'success')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"success": True})
    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of events per page
    pagination = Event.query.filter_by(user_id=current_user.id).order_by(Event.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    events = pagination.items
    return render_template('dashboard.html', events=events, pagination=pagination)