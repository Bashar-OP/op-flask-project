from flask import Flask,request,render_template,flash,redirect,url_for
import secrets



def validate(form_data):
    
    errors = []

    if not form_data['name']:
        errors.append('Name is required.')
    
    if '@' not in form_data['email']:
        errors.append( 'Email must include @.')

    if len(form_data['password']) < 8:
        errors.append( 'Password is at least 8 characters.')

    if form_data['confirm_pass'] != form_data['password']:
        errors.append( 'Confirm password must match password.')

    if form_data['bio'] and len(form_data['bio']) < 20:
        errors.append( 'Bio must be at least 20 characters if provided.')

    if not form_data['agree_terms']:
        errors.append( 'Agree to Terms must be checked.')
    
    return errors
    



app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex();


@app.route('/',methods=['GET','POST'])
def home():
    form_data = {}
    error_messages = []

    if request.method == 'GET':
        return render_template('form.html',form_data=form_data,error=error_messages)
    
    data_keys = ['name','email','password','confirm_pass','bio','agree_terms']
    

    for key in data_keys:
        form_data[key] = request.form.get(key)
    form_data['name'] = form_data['name'].strip()
    form_data['email'] = form_data['email'].strip()
    form_data['bio'] = form_data['bio'].strip() or None
    form_data['agree_terms'] = bool(form_data['agree_terms'])

    error_messages = validate(form_data)
    
    if len(error_messages) != 0 :
        return render_template('form.html',form_data=form_data,errors=error_messages)
    
    flash('success submit')
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
