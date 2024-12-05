from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
api = Api(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# 使用者模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Movie 模型
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    introduction = db.Column(db.Text, nullable=False)
    performer = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 註冊頁面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("使用者名稱已存在")
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("註冊成功，請登入")
        return redirect(url_for('login'))
    return render_template('register.html')

# 登入頁面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash("登入成功")
            return redirect(url_for('index'))
        flash("登入失敗，請檢查您的帳號和密碼")
    return render_template('login.html')

# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("登出成功")
    return redirect(url_for('index'))

# 主要頁面
@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

# 新增電影頁面
@app.route('/new_movie', methods=['GET', 'POST'])
@login_required
def new_movie():
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        introduction = request.form['introduction']
        performer = request.form['performer']
        type = request.form['type']
        new_movie = Movie(title=title, director=director, introduction=introduction, performer=performer, type=type)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_movie.html')

# 單一電影頁面
@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie.html', movie=movie)

# 編輯電影頁面
@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    if request.method == 'POST':
        movie.title = request.form['title']
        movie.director = request.form['director']
        movie.performer = request.form['performer']
        movie.type = request.form['type']
        movie.introduction = request.form['introduction']
        movie.image_url = request.form['image_url']
        db.session.commit()
        flash('電影資訊已更新！', 'success')
        return redirect(url_for('movie', movie_id=movie_id))
    
    return render_template('edit_movie.html', movie=movie)

# 刪除電影
@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 在應用程式上下文中創建資料庫
    app.run(debug=True)

