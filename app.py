from flask import Flask,render_template,request
import pickle
import numpy as np


pop_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(pop_df['Book-Title'].values),
                           book_author=list(pop_df['Book-Author'].values),
                           book_img=list(pop_df['Image-URL-M'].values),
                           book_rating=list(pop_df['Average Rating'].values),
                           book_votes=list(pop_df['Number of Ratings'].values),
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def  recommend():
    user_input=request.form.get('user_input')
    index=np.where(pt.index==user_input)[0][0]
    similar=sorted(list(enumerate(similarity[index])),key=lambda x:x[1],reverse=True)[1:6]
    data=[]
    for i in similar:
        items=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(items)
    print(data)
    return render_template('recommend.html',data=data)


if __name__=='__main__':
    app.run(debug=True)