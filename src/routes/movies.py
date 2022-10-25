from flask import Blueprint,request,Response
from ..database.models import Movie,User
from flask import jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity

movie = Blueprint("movies",__name__,url_prefix='/api/v1')

@movie.route('/movies')
@jwt_required
def movies():
    if request.method == 'GET':
        user_id = get_jwt_identity()
        movies = Movie.objects(added_by = user_id).to_json()
        return Response(movies, mimetype="application/json", status=200)
    

@movies.post('/movies')
@jwt_required
def create_movie():
    body = request.get_json()
    # movie = Movie(**body).save()  --> without jwt
    user_id = get_jwt_identity()
    user = User.objects.get(id=user_id)
    movie = Movie(**body,added_by = user).save()
    user.update(push__movie=movie)
    user.save()
    id = movie.id
    return {'id':str(id)},200
    

@movie.route('/movies/<id>',methods = ['GET', 'PUT','DELETE'])
@jwt_required
def individual_movie_action(id):
    if request.method == 'GET':
        user_id = get_jwt_identity()
        movies = Movie.objects.get(id=id,added_by = user_id).to_json()
        if not movies:
            return jsonify({"success": False,"msg":"movie not found"}),404
        return Response(movies, mimetype="application/json", status=200)
    if request.method == 'DELETE':
        user_id = get_jwt_identity()
        Movie.objects.get(id=id,added_by = user_id).delete()
        return "",200
    if request.method == 'PUT':
        body = request.get_json()
        user_id = get_jwt_identity()
        Movie.objects(id=id,added_by=user_id).update(**body)
        return '',200
