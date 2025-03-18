import os
import string
from datetime import datetime
import random
import time

from flask import *
from flask_mail import Message

from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from forms import RegisterForm, LoginForm, ResetForm, ProfileUpdateForm, GigForm, RechargeForm, RequirementForm
from models import UserModel, EmailCaptchaModel, Gig, Order, SearchModel
from exts import db, mail, register_logging
from flask import session, request
import config

app = Flask(__name__)
# app.secret_key = "sk"

app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

register_logging(app)
# @app.before_request()
# def before_request():
#     if 'user_id' in session:
#         user = UserModel.query.filter_by(id="user_id").first()


#home page
@app.route('/')
@app.route('/home')
def home():  # put application's code here
    app.logger.info('Home')
    if authentication():

        # three recommendations in the home page
        gigs = recommend(True)
        return render_template('home.html', title="home", auth=True, gigs = gigs)
    else:
        gigs = recommend(False)
        return render_template('home.html', title="home", auth=False, gigs = gigs)


# clear button on the home page that clears all the data
@app.route('/clear')
def clear():  # put application's code here
    if authentication():
        id = session.get('user.id')
        if id != None:
            User = UserModel.query.filter_by(id=id).first()

        if Order.query.all():
            for u in Order.query.all():
                db.session.delete(u)
            db.session.commit()

        if SearchModel.query.all():
            for u in SearchModel.query.all():
                db.session.delete(u)
            db.session.commit()

        if EmailCaptchaModel.query.all():
            for u in EmailCaptchaModel.query.all():
                db.session.delete(u)
            db.session.commit()

        if Gig.query.all():
            for u in Gig.query.all():
                db.session.delete(u)
            db.session.commit()

        if UserModel.query.all():
            for u in UserModel.query.all():
                db.session.delete(u)
            db.session.commit()


        app.logger.info(User.username + " cleared database and log out")

        session.clear()

        return render_template('home.html', title="home", auth=False)
    else:

        if Order.query.all():
            for u in Order.query.all():
                db.session.delete(u)
            db.session.commit()

        if SearchModel.query.all():
            for u in SearchModel.query.all():
                db.session.delete(u)
            db.session.commit()

        if EmailCaptchaModel.query.all():
            for u in EmailCaptchaModel.query.all():
                db.session.delete(u)
            db.session.commit()

        if Gig.query.all():
            for u in Gig.query.all():
                db.session.delete(u)
            db.session.commit()

        if UserModel.query.all():
            for u in UserModel.query.all():
                db.session.delete(u)
            db.session.commit()

        app.logger.info("cleared database")

        return render_template('home.html', title="home", auth=False)



# the shopping cart page
@app.route('/cart')
def cart():
    id = session.get('user.id')
    # if the user is logged in get the user
    if id != None:
        User = UserModel.query.filter_by(id=id).first()
    orders = Order.query.filter_by(buyer=User)
    uorders = []

    # just show the orders on cart
    for o in orders:
        if o.oncart == 1:
            uorders.append(o)

    app.logger.info(User.username+": cart")

    return render_template('shoppingCart.html', title="home", orders=uorders, auth=True, balance=User.balance)


# the orders page as a buyer
@app.route('/orders')
def orders():  # put application's code here
    id = session.get('user.id')
    # if the user is logged in get the user
    if id != None:
        User = UserModel.query.filter_by(id=id).first()
    orders = Order.query.filter_by(buyer=User)

    #display ongoing orders and finished orders separately
    ongoing_orders = []
    finished_orders = []
    for o in orders:
        if o.ongoing == 1:
            ongoing_orders.append(o)
        if o.finished == 1:
            finished_orders.append(o)

    app.logger.info(User.username + ": orders as a buyer")

    return render_template('Orders.html', title="home", ongoing=ongoing_orders, finished=finished_orders, auth=True)


# the orders page as a seller
@app.route('/orders_seller')
def orders_seller():
    id = session.get('user.id')
    # if the user is logged in get the user
    if id != None:
        User = UserModel.query.filter_by(id=id).first()
    orders = Order.query.all()
    orders_seller = []

    for oo in orders:
        if oo.gig.author == User:
            orders_seller.append(oo)


    ongoing_orders = []
    finished_orders = []
    for o in orders_seller:
        if o.ongoing == 1:
            ongoing_orders.append(o)
        if o.finished == 1:
            finished_orders.append(o)

    app.logger.info(User.username + ": orders as a seller")


    return render_template('orders_seller.html', title="seller", ongoing=ongoing_orders, finished=finished_orders, auth=True)



# check others' profile ,
@app.route('/<int:user_id>')
def othersProfile(user_id):

    id = session.get('user.id')
    # if the user is logged in get the user
    if id != None:
        current_user = UserModel.query.filter_by(id=id).first()
    if authentication():

        User = UserModel.query.filter_by(id=user_id).first()
        gigs = Gig.query.filter_by(user_id=user_id)
        user = User

        #if is the user himself, show the user's profile page
        if current_user == user:
            app.logger.info(User.username + ": check other's profile(self)")
            return redirect(url_for("profile"))
        else:

            # get the avatar of the person
            root_dir = '/Users/azalea/team_16-main'
            # root_dir = 'C:/Users/12716/Desktop/team_16 5'
            # os.path.dirname('app.py')os.path.abspath()
            # root_dir = os.path.abspath(os.path.dirname('app.py'))
            file_path = root_dir + '/static' + '/avatar'
            files = os.listdir(file_path)
            for i in range(len(files)):
                print(i)
                if files[i] != user.avatar:
                    pass
                else:
                    break
            avatar = "/static/avatar/" + files[i]
            app.logger.info(" check" + user.username+"'s profile")

            return render_template('check_others_profile.html', title="home", auth=True, u=User, gigs=gigs, avatar=avatar)


    else:

        # visitors
        User = UserModel.query.filter_by(id=user_id).first()
        gigs = Gig.query.filter_by(user_id=user_id)
        user = User
        # root_dir = '/Users/azalea/Desktop/team_16 5'
        # root_dir = 'C:/Users/12716/Desktop/team_16 5'
        # os.path.dirname('app.py')os.path.abspath()
        # root_dir = os.path.abspath(os.path.dirname('app.py'))
        root_dir = '/Users/azalea/team_16-main'
        file_path = root_dir + '/static' + '/avatar'
        files = os.listdir(file_path)
        for i in range(len(files)):
            print(i)
            if files[i] != user.avatar:
                pass
            else:
                break
        avatar = "/static/avatar/" + files[i]
        app.logger.info(" check" + user.username + "'s profile")
    return render_template('check_others_profile.html', title="home", auth=False, u=User, gigs=gigs, avatar=avatar)



# the shopping page
@app.route('/shopping/<int:gig_id>', methods=['GET', 'POST'])
def shopping(gig_id):  # put application's code here

    gig = Gig.query.get_or_404(gig_id)
    form = RequirementForm(request.form)
    if request.method == 'GET':
        app.logger.info("shopping")
        return render_template('shoppingPage.html', title="shopping", gig=gig, auth=True, form=form)
    else:
        id = session.get('user.id')
        # if the user is logged in get the user
        if id != None:
            User = UserModel.query.filter_by(id=id).first()

        # create an order with requirement
        if form.validate():
            order = Order(buyer=User, gig=gig, price=gig.price, requirement=form.content.data, oncart=1)
            db.session.add(order)
            db.session.commit()
            app.logger.info(User.username + "shopping and add to cart")
            return redirect(url_for("cart"))
        else:
            app.logger.warning("Did not enter requirement while adding to cart")
            flash("Please enter your requirement!", "danger")
            return render_template('shoppingPage.html', title="shopping", gig=gig, auth=True, form=form)


# register page

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        app.logger.info("Register")
        return render_template("register.html", title='register')
    else:
        form = RegisterForm(request.form)
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # print(form.errors)

        print(email, username, password)

        # encrypt password
        passw_hash = generate_password_hash(form.password.data)

        if form.validate():
            user = UserModel(email=email, username=username, password=passw_hash)
            db.session.add(user)
            db.session.commit()

            print("validate success")
            app.logger.info(username+" : account created")
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for("login"))
        else:
            print("validate fail")
            app.logger.warning(username + " : Did not provide validate form for register")
            return redirect(url_for("register"))


# create gig
@app.route('/creategig', methods=['GET', 'POST'])
def create_gig():
    form = GigForm()
    id = session.get('user.id')
    # if the user is logged in get the user
    if id != None:
        User = UserModel.query.filter_by(id=id).first()
    if form.validate_on_submit():

        # store the uploaed picture
        if form.pic.data is not None:
            print("pic!!!!!")
            filename = secure_filename(form.pic.data.filename)
            nowTime = datetime.now().strftime("%Y%m%d%H%M%S")
            randomNum = random.randint(10, 99)
            uniqueNum = str(nowTime) + str(randomNum)
            # root_dir = "/Users/azalea/Desktop/team_16 4"
            # form.pic.data.save(root_dir + '/static/pic/' + uniqueNum + "_" + filename)
            # root_dir = os.path.abspath(os.path.dirname('app.py'))
            # root_dir = "C:/Users/12716/Desktop/team_16 5"
            root_dir = '/Users/azalea/team_16-main'
            # root_dir = '/Users/azalea/Desktop/team_16 5'
            form.pic.data.save(root_dir + '/static/pic/' + uniqueNum + "_" + filename)
            pic_name = uniqueNum + "_" + filename
        else:
            pic_name = ""

        print(form.module.data)
        # create a new gig and add it to the database
        gig = Gig(content=form.content.data, author=User, pic=pic_name, title=form.title.data, module=form.module.data,
                  price=form.price.data)
        db.session.add(gig)
        db.session.commit()

        app.logger.info("New gig created for" + User.username+" in the module "+gig.module)
        flash('Your gig has been created!', 'success')

        if form.module.data == "Cartoon":
            return redirect(url_for('cartoon_page'))
        elif form.module.data == "Cure":
            return redirect(url_for('cure_page'))
        elif form.module.data == "Fan Fiction":
            return redirect(url_for('fan_page'))
        else:
            form.module.data == "Style Painting"
            return redirect(url_for('style_page'))

    else:
        flash('Please enter validate input!', 'danger')
        app.logger.warning("Did not provide validate input for gig creation")
        try:
            print(form.errors)
        except:
            pass

    return render_template('createNewGig.html', title="createGig", form=form, auth=True)


#  search for gigs related to the given word
@app.route('/search', methods=['post', 'get'])
def search():
    id = session.get('user.id')
    # if the user is logged in get the user
    if id != None:
        User = UserModel.query.filter_by(id=id).first()
    content = request.form.get('content')
    if content is None:
        content = " "
    else:
        if authentication():
            if len(content.split()) != 0:
                search = SearchModel(content=content, user_id=User.id, num=1)
                s = SearchModel.query.filter_by(content=content).first()

                # add to the number to keep the searched time
                if s is None:
                    db.session.add(search)
                else:
                    if s.user_id == User.id:
                        s.num += 1
                        s.search_time = datetime.now()
                    else:
                        db.session.add(search)

                    print(content)
                    print(s.num)

                db.session.commit()

    # selection search, searching for the matching content and title
    select = request.form.get('select')
    app.logger.info("Searching results for: "+content+" in the module of: "+select)
    if select == "Cure":
        # gigs = Gig.query.filter_by(module="Cure")
        # return render_template('cureClass.html', title="CurePage", auth=True, gigs=gigs)
        Gigs = Gig.query.filter(Gig.content.like("%" + content + "%") if content is not None else "").all()
        g2 = Gig.query.filter(Gig.title.like("%" + content + "%") if content is not None else "").all()

        for g in g2:
            if g not in Gigs:
                Gigs.append(g)
        gs = []
        for gg in Gigs:
            if gg.module == select:
                gs.append(gg)
        if authentication():
            return render_template('SearchPage.html', title="CurePageSearch", auth=True, gigs=gs)
        else:
            return render_template('SearchPage.html', title="CurePageSearch", auth=False, gigs=gs)

    if select == "Cartoon":
        # gigs = Gig.query.filter_by(module="Cure")
        # return render_template('cureClass.html', title="CurePage", auth=True, gigs=gigs)
        Gigs = Gig.query.filter(Gig.content.like("%" + content + "%") if content is not None else "").all()
        g2 = Gig.query.filter(Gig.title.like("%" + content + "%") if content is not None else "").all()

        for g in g2:
            if g not in Gigs:
                Gigs.append(g)
        gs = []
        for gg in Gigs:
            if gg.module == select:
                gs.append(gg)
        if authentication():
            return render_template('SearchPage.html', title="CartoonPageSearch", auth=True, gigs=gs)
        else:
            return render_template('SearchPage.html', title="CartoonPageSearch", auth=False, gigs=gs)

    if select == "Fan Fiction":
        # gigs = Gig.query.filter_by(module="Cure")
        # return render_template('cureClass.html', title="CurePage", auth=True, gigs=gigs)
        Gigs = Gig.query.filter(Gig.content.like("%" + content + "%") if content is not None else "").all()
        g2 = Gig.query.filter(Gig.title.like("%" + content + "%") if content is not None else "").all()

        for g in g2:
            if g not in Gigs:
                Gigs.append(g)
        gs = []
        for gg in Gigs:
            if gg.module == select:
                gs.append(gg)
        if authentication():
            return render_template('SearchPage.html', title="FanPageSearch", auth=True, gigs=gs)
        else:
            return render_template('SearchPage.html', title="FanPageSearch", auth=False, gigs=gs)

    if select == "Style Painting":
        # gigs = Gig.query.filter_by(module="Cure")
        # return render_template('cureClass.html', title="CurePage", auth=True, gigs=gigs)
        Gigs = Gig.query.filter(Gig.content.like("%" + content + "%") if content is not None else "").all()
        g2 = Gig.query.filter(Gig.title.like("%" + content + "%") if content is not None else "").all()


        for g in g2:
            if g not in Gigs:
                Gigs.append(g)
        gs = []
        for gg in Gigs:
            if gg.module == select:
                gs.append(gg)
        if authentication():
            return render_template('SearchPage.html', title="StylePageSearch", auth=True, gigs=gs)
        else:
            return render_template('SearchPage.html', title="StylePageSearch", auth=False, gigs=gs)

    else:
        Gigs = Gig.query.filter(Gig.content.like("%" + content + "%") if content is not None else "").all()
        g2 = Gig.query.filter(Gig.title.like("%" + content + "%") if content is not None else "").all()

        for g in g2:
            if g not in Gigs:
                Gigs.append(g)
        if authentication():
            return render_template('SearchPage.html', title="AllPageSearch", auth=True, gigs=Gigs)
        else:
            return render_template('SearchPage.html', title="AllPageSearch", auth=False, gigs=Gigs)



# recharge balance
@app.route("/recharge", methods=['GET', 'POST'])
def recharge():
    if request.method == "GET":
        return redirect(url_for('profile'))
    else:
        form = RechargeForm(request.form)
        if form.validate():
            id = session.get('user.id')
            # if the user is logged in get the user
            if id != None:
                User = UserModel.query.filter_by(id=id).first()
                # add to the current balance
                User.balance = User.balance + int(form.content.data)

                db.session.commit()
                app.logger.info("(Successful) after Recharged :"+str(User.balance))
        else:
            app.logger.warning("Recharge failed because more than 10000")
            flash("Please charge below 10000 at a time", "danger")

    return redirect(url_for('profile'))

# change the privacy settings for email
@app.route('/changeEmail', methods=["GET", "POST"])
def changeEmail():
    id = session.get('user.id')
    # if the user is logged in get the user
    if id != None:
        User = UserModel.query.filter_by(id=id).first()
    seeable = User.seeEmail

    # 1 could see, 0 could not see
    print(seeable)
    if seeable == 1:
        seeable = 0
    else:
        seeable = 1
    User.seeEmail = seeable
    db.session.commit()
    app.logger.info("Changed email privacy")
    return jsonify({"code": 200})




# a temporary list use for making a deal in the shopping cart page, just temporary so not threats
current_orders = []


# place the order in the shopping cart the the dealing list
@app.route('/placeOrder', methods=['GET', 'POST'])
def placeOrder():
    if request.method == 'POST':
        data = request.get_json()
        # print(data)
        # print(type(data['name']))
        # print(data['name'])
        #cat ID: 4
        result = data['name']
        l = result.split()
        order_id = int(l[2])
        print(l)

        current_orders.append(order_id)
        print(current_orders)
        app.logger.info("added order to current deal list")
        return jsonify({'status': 200, 'msg': 'Added to the current deal'})
    else:
        return 'error'


# purchase the orders in the dealing list
@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        data = request.get_json()
        # print(data)

        # get the sum of the fee
        totalmoney = data['totalmoney']

        id = session.get('user.id')
        # if the user is logged in get the user
        if id != None:
            User = UserModel.query.filter_by(id=id).first()
        if User:
            balance = User.balance
            # check if balance is enough
            if balance > int(totalmoney) or balance == int(totalmoney):
                User.balance = balance - int(totalmoney)

                # find the orders in the list and make it leave the cart to ongoing orders
                for order_id in current_orders:
                    order = Order.query.filter_by(id=order_id).first()
                    order.oncart = 0
                    order.ongoing = 1
                    db.session.commit()
                    print(order_id)

                print(totalmoney)

                # clear the list
                current_orders.clear()
                app.logger.info("Paid successfully at price "+totalmoney)
                return jsonify({'status': 200, 'msg': 'Successful Payment!'})
            else:
                print("failed")
                app.logger.warning("The balance is not enough for paying")
                return jsonify({'status': 400, 'msg': 'Your balance is not enough, please recharge first!'})



    else:
        return redirect(url_for("orders"))


# clear the list when the clear button on the dealing page is pressed

@app.route("/clear", methods=['POST'])
def clearList():
    current_orders.clear()
    app.logger.info("cleared current deal")

    return jsonify({"code": 200})


#as a seller, finish the order in the ongoing orders
@app.route("/finishorder", methods=['POST'])
def finish():
    order_id = request.form.get("order_id")

    order = Order.query.filter_by(id=order_id).first()  # change
    order.ongoing = 0
    order.finished = 1
    db.session.commit()
    app.logger.info("Finished the order: "+order_id)

    return jsonify({"code": 200})


# cartoon page with gigs
@app.route('/cartoon_page')
def cartoon_page():
    app.logger.info("Browse cartoon page")
    # get gigs in order to display all the gigs in the cartoon category later
    # if the user is logged in
    # gigs = Gig.query.order_by(db.text("-date_posted"))
    if authentication():
        gigs = Gig.query.filter_by(module="Cartoon")

        return render_template('cartoonClass.html', title="CartoonPage", auth=True, gigs=gigs)
    else:
        gigs = Gig.query.filter_by(module="Cartoon")
        return render_template('cartoonClass.html', title="CartoonPage", auth=False, gigs=gigs)


# cure page with gigs
@app.route('/cure_page')
def cure_page():
    app.logger.info("Browse cure page")
    # get gigs in order to display all the gigs in the cartoon category later
    # if the user is logged in
    # gigs = Gig.query.order_by(db.text("-date_posted"))
    if authentication():
        gigs = Gig.query.filter_by(module="Cure")
        return render_template('cureClass.html', title="CurePage", auth=True, gigs=gigs)
    else:
        gigs = Gig.query.filter_by(module="Cure")
        return render_template('cureClass.html', title="CurePage", auth=False, gigs=gigs)


# fan fiction page with gigs
@app.route('/fan_fiction_page')
def fan_page():
    app.logger.info("Browse fan fiction page")
    # get gigs in order to display all the gigs in the cartoon category later
    # if the user is logged in
    # gigs = Gig.query.order_by(db.text("-date_posted"))
    if authentication():
        gigs = Gig.query.filter_by(module="Fan Fiction")
        return render_template('FanClass.html', title="CartoonPage", auth=True, gigs=gigs)
    else:
        gigs = Gig.query.filter_by(module="Fan Fiction")
        return render_template('FanClass.html', title="CartoonPage", auth=False, gigs=gigs)


# style painting page with gigs
@app.route('/style_painting_page')
def style_page():
    app.logger.info("Browse style painting page")
    # get gigs in order to display all the gigs in the cartoon category later
    # if the user is logged in
    # gigs = Gig.query.order_by(db.text("-date_posted"))
    if authentication():
        gigs = Gig.query.filter_by(module="Style Painting")
        return render_template('StyleClass.html', title="CartoonPage", auth=True, gigs=gigs)
    else:
        gigs = Gig.query.filter_by(module="Style Painting")
        return render_template('StyleClass.html', title="CartoonPage", auth=False, gigs=gigs)


# single gig page
@app.route('/module_page/<int:gig_id>', methods=["GET", "POST"])
def gig_page_single(gig_id):
    # get the particular gig
    gig = Gig.query.get_or_404(gig_id)
    # if the user is logged in

    app.logger.info("Browse single gig page of ID: "+str(gig.id))
    if authentication():
        return render_template('viewPage.html', title="CartoonPage", auth=True, gig=gig)
    else:
        return render_template('viewPage.html', title="CartoonPage", auth=False, gig=gig)


# logout
@app.route('/logout', methods=["POST", "GET"])
def logout():
    app.logger.info("logout successfully")
    session.clear()  # clear the session
    return redirect(url_for("login"))


# login page
@app.route('/login', methods=["POST", "GET"])
def login():  # put application's code here
    if request.method == "GET":
        app.logger.info("Try to login")
        return render_template("login.html")
    else:

        if session.get('user.id') != None:
            session.pop('user.id')

        print(session.get('user.id'))
        form = LoginForm(request.form)

        # form validation
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            # if user and user.password == password:

            #check password
            if user and check_password_hash(user.password, password):
                # login_user(user, remember=form.remember.data)
                session['user.id'] = user.id
                print(session.get('user.id'))
                flash('You log in!', "success")

                app.logger.info("Login successfully for "+user.username)
                return redirect(url_for('home'))
            else:

                flash("The password does not match, check the email address or password", 'danger')
                return redirect(url_for('login'))

        else:
            app.logger.warning("Login failed due to input validation")
            flash("The form of email address or password is incorrect", 'danger')

    return render_template('login.html', title="login")

# reset password page
@app.route("/resetpsw", methods=['GET', 'POST'])
def reset():
    if request.method == 'GET':
        app.logger.info("Trying to reset password")
        return render_template("forgetpsw.html", title='Reset Password')
    else:
        form = ResetForm(request.form)
        email = form.email.data
        password = form.password.data
        # encrypt user passwords
        hash_password = generate_password_hash(password)
        if form.validate():
            if email:
                user = UserModel.query.filter_by(email=email).first()
                # check whether the user exist or not
                if user:
                    user.password = hash_password
                    # user.create_time = datetime.now()
                    db.session.commit()
                    flash('Login: Password has successfully changed!', 'success')
                    app.logger.info("Reset password successfully for "+user.username)
                    return redirect(url_for("login"))
                else:
                    app.logger.warning("Reset password failed, need to register first")
                    flash('You haven\'t registered, please sign up first')
                    return redirect(url_for("reset"))
            else:
                app.logger.warning("Reset password failed, did not enter email")
                flash('Please enter your email')
                return redirect(url_for("reset"))
        else:
            app.logger.warning("Reset password failed, did not enter validate form")

            return redirect(url_for("reset"))


# the profile page of the current user
@app.route('/profile', methods=["POST", "GET"])
def profile():
    id = session.get('user.id')
    form = ProfileUpdateForm()
    if authentication():
        if id != None:
            User = UserModel.query.filter_by(id=id).first()
            if request.method == "GET":
                # get the avatar and display
                user = User
                root_dir = '/Users/azalea/team_16-main'
                # root_dir = os.path.abspath(os.path.dirname('app.py'))
                # root_dir = '/Users/azalea/Desktop/team_16 5'
                # root_dir = 'C:/Users/12716/Desktop/team_16 5'
                # os.path.dirname('app.py')os.path.abspath()
                file_path = root_dir + '/static' + '/avatar'
                files = os.listdir(file_path)
                for i in range(len(files)):
                    print(i)
                    if files[i] != user.avatar:
                        pass
                    else:
                        break
                avatar = "/static/avatar/" + files[i]
                print(avatar)

                gigs = Gig.query.filter_by(user_id=id)
                app.logger.info("Checking profile")
                return render_template('profile.html', form=form, title='Go Now', avatar=avatar, u=User,
                                       auth=True, gigs=gigs)
            else:

                #submit new avatar
                profile_model = User
                print("form.data",form.avatar.data)
                if form.avatar.data is not None:
                    print(1)
                    filename = secure_filename(form.avatar.data.filename)
                    nowTime = datetime.now().strftime("%Y%m%d%H%M%S")
                    randomNum = random.randint(0, 99)
                    uniqueNum = str(nowTime) + str(randomNum)
                    root_dir = '/Users/azalea/team_16-main'
                    # root_dir = os.path.abspath(os.path.dirname('app.py'))
                    form.avatar.data.save(root_dir+'/static/avatar/' + uniqueNum + "_" + filename)
                    # form.avatar.data.save('C:/Users/12716/Desktop/team_16 5/static/avatar/' + uniqueNum + "_" + filename)
                    file_name = uniqueNum + "_" + filename
                    app.logger.info("Changed profile avatar")
                else:
                    app.logger.info("Did not provide profile avatar, given default image")
                    file_name = "default_avatar.png"
                if profile_model:
                    profile_model.avatar = file_name
                    db.session.commit()
                return redirect(url_for("profile"))

        else:
            return redirect(url_for("home"))
    else:
        return render_template("login.html")


# check login status
def authentication():
    if session.get('user.id'):
        return True
    else:
        return False

# get email captcha
@app.route('/captcha/', methods=["POST"])
def get_captcha():  # get the captcha
    print("captcha")
    letters = string.ascii_letters + string.digits  # get the letters and digits
    captcha = "".join(random.sample(letters, 6))  # get the captcha

    email = request.form.get("email")  # get the email address

    if email:  # if the email address is not empty
        # send the email

        message = Message(
            subject="[Art Finder] Registration Verification",
            recipients=[email],
            body=f"[Art Finder]: Your captcha code is {captcha}, please complete the verification within 10 "
                 "minutes "
        )
        mail.send(message)
        # add the captcha to the database
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print(captcha)

        app.logger.info("Sent email captcha : "+captcha)
        return jsonify({"code": 200})
    else:  # if the email address is empty
        app.logger.warning("Could not send captcha email because email is not entered")
        return jsonify({"code": 400, "message": "Please enter your email address"})  # return the error message






# check whether the username exist or not when registering
@app.route('/checkuser', methods=['POST'])
def check_username():
    app.logger.info("Checking username")
    # print(request)
    time.sleep(2)
    chosen_name = request.form['username']
    user_in_db = UserModel.query.filter_by(username=chosen_name).first()
    check = user_in_db == None
    # print(check)
    if check:
        app.logger.info("Username is available")
        return jsonify({'text': 'Username is available',
                        'returnvalue': 0})
    else:
        app.logger.warning("Username is taken")
        return jsonify({'text': 'Sorry! Username is already taken',
                        'returnvalue': 1})



# show gigs using ajax on the profile page
@app.route('/show_gigs', methods=['POST'])
def show_gigs():
    print(request)
    if request.method == 'POST':
        data = request.get_json()
        # print(data)
        authorId = data['authorId']
        authorId = int(authorId)
        print(authorId)
        print(type(authorId))
        gigs = Gig.query.filter_by(user_id=authorId)
        gigList = []
        for gig in gigs:
            gig_pic = gig.pic
            gig_title = gig.title
            id = session.get('user.id')
            # if the user is logged in get the user
            if id != None:
                User = UserModel.query.filter_by(id=id).first()
            author_name = User.username
            print(author_name)
            gig_price = gig.price

            gig_content = gig.content
            gig_id = gig.id
            gigdic = {'gig_pic':gig_pic,
                      'gig_title':gig_title,
                      'gig_price':gig_price,
                      "gig_author_name":author_name,
                      'gig_content':gig_content,
                      'gig_id':gig_id}
            gigList.append(gigdic)
            app.logger.info("Show gigs")

        return jsonify({'gigList':gigList,'msg': 'success'})
    else:
        return 'error'


# provide recommendations of gigs on the home page
def recommend(s):
        if s == True:
            id = session.get('user.id')
            search2 = SearchModel.query.filter_by(user_id=id).order_by(db.text("-search_time")).all()
            result_gigs = []
            search = []

            # find out the top three searched word out of 5 recently searched words

            # recently searched 5 words
            if len(search2) < 5:
                for p in search2:
                    search.append((p, p.num))
            else:
                i = 0
                while i < 5:
                    search.append((search2[i], search2[i].num))
                    i += 1
            search.sort(key=lambda x: x[1])
            search.reverse()

            # search = [[SearchModel,Searched number],[x,x]]
            if len(search) < 3:
                search = search
            else:
                search = search[0:3]

            j = 0
            while j < 3:
                if len(search) > 0:
                    if j < len(search):

                        print(search[j][0].content)
                        Gigs = Gig.query.filter(
                            Gig.content.like("%" + search[j][0].content + "%") if search[j] is not None else "").all()
                        Gigs2 = Gig.query.filter(
                            Gig.title.like("%" + search[j][0].content + "%") if search[j] is not None else "").all()

                        Gigs3 = Gig.query.filter(
                            Gig.module.like("%" + search[j][0].content + "%") if search[j] is not None else "").all()
                        Gigs2 += Gigs3

                        for g in Gigs2:
                            if g not in Gigs:
                                Gigs.append(g)
                        gs = []
                        for p in Gigs:
                            gs.append(p)
                        gs.reverse()
                        result_gigs += gs

                j += 1
            rg =[]
            for r in result_gigs:
                if r not in  rg:
                    rg.append(r)

            return rg[0:3]

        #for visitors
        else:

            # for every searched words
            search2 = SearchModel.query.order_by(db.text("-search_time")).all()
            result_gigs = []
            search = []

            # find out the top three searched word out of 5 recently searched words

            # recently searched 5 words
            if len(search2) < 5:
                for p in search2:
                    search.append((p, p.num))
            else:
                i = 0
                while i < 5:
                    search.append((search2[i], search2[i].num))
                    i += 1
            search.sort(key=lambda x: x[1])
            search.reverse()

            # search = [[SearchModel,Searched number],[x,x]]
            if len(search) < 3:
                search = search
            else:
                search = search[0:3]

            j = 0
            while j < 3:  # top 3 NOT SCIENTIFIC
                if len(search) > 0:
                    if j < len(search):
                        Gigs = Gig.query.filter(
                            Gig.content.like("%" + search[j][0].content + "%") if search[j] is not None else "").all()
                        Gigs2 = Gig.query.filter(
                            Gig.title.like("%" + search[j][0].content + "%") if search[j] is not None else "").all()

                        Gigs3 = Gig.query.filter(
                            Gig.module.like("%" + search[j][0].content + "%") if search[j] is not None else "").all()
                        Gigs2 += Gigs3

                        for g in Gigs2:
                            if g not in Gigs:
                                Gigs.append(g)
                        gs = []
                        for p in Gigs:
                            gs.append(p)
                        gs.reverse()
                        result_gigs += gs

                j += 1
            rg = []
            for r in result_gigs:
                if r not in rg:
                    rg.append(r)

            return rg[0:3]

@app.route('/404')
def index404():
    abort(404)
    return 'hello world'


@app.errorhandler(404)
def err_handler_404(e):
    app.logger.error("404")
    return '404-Not Found'

@app.errorhandler(500)
def err_handler_500(e):
    app.logger.error("500")
    return '500-Internal Server Error'

@app.errorhandler(401)
def err_handler_401(e):
    app.logger.error("401")
    return '401-Unauthorised'



@app.errorhandler(400)
def err_handler_400(e):
    app.logger.error("400")
    return '400-Bad Request'




@app.errorhandler(403)
def err_handler_403(e):
    app.logger.error("403")
    return '403-Forbidden'

@app.errorhandler(502)
def err_handler_403(e):
    app.logger.error("502")
    return '502-Service Temporarily Overloaded'


@app.errorhandler(503)
def err_handler_503(e):
    app.logger.error("504")
    return '503-Service Unavailable'

if __name__ == '__main__':
    app.run(debug=True)
