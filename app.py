from bson import ObjectId
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.ehc0xum.mongodb.net/?retryWrites=true&w=majority' ,)
db = client.dbsparta
import logging  #python에서 콜솔로그를 찍기위한 import라고한다.


@app.route('/')
def home():
    return render_template('index.html')
#detail페이지이동
@app.route('/detail')
def detail():
    return render_template('detail.html')
@app.route('/addTeam')
def addTeam():
    return render_template('addTeam.html')
#댓글 닉네임 등록
@app.route('/comment', methods=["POST"])
def comment_post():
    nickname_receive = request.form['nickname_give']
    #입력한 nickname 가져와서 저장
    comment_receive = request.form['comment_give']
    #입력한 코멘트 가져와서 저장
    user_id = request.form['user_id_give']
    doc = {
        'comment' : comment_receive,
        'nickname' : nickname_receive,
        'user_id' : user_id
    }
    #dictionary형태로 저장
    db.lucky_comment.insert_one(doc)
    
    return jsonify({'msg' : '댓글 등록 완료!'})#성공시 메세지출력
#댓글 수정
@app.route('/comment', methods=["PUT"])
def update_comment():
    #닉네임 받아오기
    nickname2 = request.form['nickname2_update3']
    #댓글 받아오기
    comment2 = request.form['comment2_update3']
    #id 받아오기
    _id_receive = request.form['_id_update3']
    _id = ObjectId(_id_receive)
    #id가 string값이므로 다시한번 ObjectID로 바꿔주는 코드
    db.lucky_comment.update_many({'_id':_id}, {'$set' : {'nickname' : nickname2,
                                                           'comment' : comment2}}, upsert=True)

    return jsonify({'msg' : '댓글 수정 완료!'})
#댓글 가져오기
@app.route("/comment", methods=["GET"])
def comment_get():
    all_comment = list(db.lucky_comment.find({},))
    for con in all_comment:
        con['_id'] = str(con['_id'])
    #ObjectID형인 _id를 가져오지 못해 반복문으로 일일이 문자열으로 바꿔서 가져오는 코드
    
    return jsonify({'result': all_comment}) # 저장한 값 반환
#상세 페이지 이미지, 이름 내려주기

@app.route('/comment', methods=["DELETE"])
def delete_comment():
    _id_receive = request.form['_id_give']
    _id = ObjectId(_id_receive)
    db.lucky_comment.delete_one({'_id':_id})
    return jsonify({'msg':'삭제 완료!'})

@app.route("/introduction", methods=["GET"])
def get_users():
    all_images = list(db.lucky_users.find({},))
    for user in all_images:
        user['_id'] = str(user['_id'])
    # MongoDB의 find() 메서드를 사용하여 모든 문서를 조회하고, 결과로 반환되는 문서들 중에서 _id 필드는 제외하고 img_url, name 필드만 가져오도록 설정
    return jsonify({'result': all_images})

#메인페이지 이미지 이름 가져오기
@app.route("/index", methods=["GET"])
def main_get():
    all_users = list(db.lucky_users.find({},))
    for user in all_users:
        user['_id'] = str(user['_id'])
    #ObjectID형인 _id를 가져오지 못해 반복문으로 일일이 문자열으로 바꿔서 가져오는 코드
    
    return jsonify({'result': all_users}) # 저장한 값 반환

#팀원 등록
@app.route('/introduction', methods=["POST"])
def post():
    #이미지url 받아오기
    img_url = request.form['img_url_give']
    #이름 받아오기
    name = request.form['name_give']
    #소개1 받아오기
    introduce_1 = request.form['introduce_1_give']
    #소개2 받아오기
    

    doc = {
        'img_url' : img_url,
        'name' : name,
        'introduce': introduce_1
        
    }
    #dictionary형태로 저장
    db.lucky_users.insert_one(doc)
    

    return jsonify({'msg' : '팀원추가 완료!'})#성공시 메세지 출력
#팀원 삭제
@app.route('/introduction', methods=["DELETE"])
def delete_user():
    _id_receive = request.form['_id_give']
    _id = ObjectId(_id_receive)
    db.lucky_users.delete_one({'_id':_id})
    return jsonify({'msg':'삭제 완료!'})
@app.route('/introduction', methods=["PUT"])
def update_profile():
    #이미지url 받아오기
    img_url3 = request.form['url_update']
    #이름 받아오기
    name3 = request.form['name_update']
    #소개1 받아오기
    introduce_u1 = request.form['comment2_update']
    #_id 값 받아오고 ObjectId로 형변환 하기
    _id_receive3 = request.form['_id_update']
    _id2 = ObjectId(_id_receive3)

    db.lucky_users.update_many({'_id':_id2}, {'$set' : {'name' : name3,
                                                           'img_url' : img_url3,
                                                            'introduce' : introduce_u1}},
                                                              upsert=True)
    return jsonify({'msg' : '프로필 수정 완료!'})
if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True)