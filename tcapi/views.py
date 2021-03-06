from django.shortcuts import render
from django.contrib.auth.models import User
from django.http.response import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from tcapi.models import Posts, PostReactions, CommentReplies
from tcapi.serializers import UserSerializer, UserSerializerWithToken, PostsSerializer, CommentRepliesSerializer, PostReactionsSerializers



@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get, put, or delete all users
@api_view(["GET", "PUT", "DELETE"])
def user_list(request):
    if request.method == "GET":
        users = User.objects.all()

        username = request.GET.get("username", None)
        if username is not None:
            users = users.filter(username__icontains=username)

        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == "PUT":
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        count = User.objects.all().delete()
        return JsonResponse(
            {"message": "{} Users were deleted successfully!".format(count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )

# search users by email address
@api_view(["GET", "PUT", "DELETE"])
def all_users_by_email(request):
    """
    This view gets all user's stored in the database by their email.
    """
    if request.method == "GET":
        users = User.objects.all()

        email = request.GET.get("email", None)
        if email is not None:
            users = users.filter(email__icontains=email)

        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == "PUT":
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        count = User.objects.all().delete()
        return JsonResponse(
            {"message": "{} Users were deleted successfully!".format(count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )

# Find a user by their ID
@api_view(["GET", "PUT", "DELETE"])
def user_detail(request, pk):
    # find user by pk (id)
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse(
            {"message": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    # GET / PUT / DELETE
    if request.method == "GET":
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)

    if request.method == "PUT":
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data)
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get Put or Delete all tweets
@api_view(["GET", "PUT", "DELETE"])
def tweet_list(request):
    if request.method == "GET":
        tweets = Posts.objects.all()

        tweet = request.GET.get("tweet", None)
        if tweet is not None:
            tweets = tweets.filter(tweet__icontains=tweet)

        posts_serializer = PostsSerializer(tweets, many=True)
        return JsonResponse(posts_serializer.data, safe=False)
    elif request.method == "PUT":
        tweets_data = JSONParser().parse(request)
        posts_serializer = PostsSerializer(data=tweets_data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            return JsonResponse(posts_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        count = Posts.objects.all().delete()
        return JsonResponse(
            {"message": "{} Posts were deleted successfully!".format(count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )
        return JsonResponse({
            "message":"This is from tweet_list"
        },status=status.HTTP_206_PARTIAL_CONTENT)


# user authorization
@api_view(["POST", "DELETE"])
def post_tweet_auth_user(request):
    if request.method == "POST":
        post_tweet = JSONParser().parse(request)
        posts_serializer = PostsSerializer(data=post_tweet)
        if posts_serializer.is_valid():
            posts_serializer.save()
            return JsonResponse(posts_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get a specific tweet by username
@api_view(["GET", "PUT", "DELETE"])
def tweet_detail(request, pk):

    # GET / PUT / DELETE
    if request.method == "GET":
        # find post by pk (id)
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            return JsonResponse(
                {"message": "The post does not exist"}, status=status.HTTP_404_NOT_FOUND
            )


        post_serializer = PostsSerializer(post)
        return JsonResponse(post_serializer.data)

# Get all post reactions
@api_view(["GET", "PUT", "DELETE"])
def postreactions_list(request):
    if request.method == "GET":
        reactions = PostReactions.objects.all()

        reactioncomments = request.GET.get("reactioncomments", None)
        if tweet is not None:
            reactioncomments = reactioncomments.filter(
                reactioncomments__icontains=reactioncomments
            )

        postreactions_serializer = PostReactionsSerializer(reactioncomments, many=True)
        return JsonResponse(postreactions_serializer.data, safe=False)
    elif request.method == "PUT":
        postreactions_data = JSONParser().parse(request)
        postreactions_serializer = PostReactionsSerializer(data=postreactions_data)
        if postreactions_serializer.is_valid():
            postreactions_serializer.save()
            return JsonResponse(
                postreactions_serializer.data, status=status.HTTP_201_CREATED
            )
        return JsonResponse(
            postreactions_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == "DELETE":
        count = PostReactions.objects.all().delete()
        return JsonResponse(
            {
                "message": "{} Post reactions were deleted successfully!".format(
                    count[0]
                )
            },
            status=status.HTTP_204_NO_CONTENT,
        )

# get a post reaction by id
@api_view(["GET", "PUT", "DELETE"])
def postreactions_detail(request, pk):
    # find postreaction by pk (id)
    try:
        postreaction = PostReactions.objects.get(pk=pk)
    except PostReactions.DoesNotExist:
        return JsonResponse(
            {"message": "The post does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    # GET / PUT / DELETE
    if request.method == "GET":
        postreactions_serializer = PostReactionsSerializer(postreaction)
        return JsonResponse(postreactions_serializer.data)

    if request.method == "PUT":
        postreaction_data = JSONParser().parse(request)
        postreactions_serializer = PostReactionsSerializer(
            postreaction, data=postreaction_data
        )
        if postreactions_serializer.is_valid():
            postreactions_serializer.save()
            return JsonResponse(postreactions_serializer.data)
        return JsonResponse(
            postreactions_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

# get a list of all comment replies
@api_view(["GET", "PUT", "DELETE"])
def commentreplies_list(request):
    if request.method == "GET":
        commentreplies = CommentReplies.objects.all()

        postcomments = request.GET.get("postcomments", None)
        if tweet is not None:
            postcomments = postcomments.filter(postcomments__icontains=postcomments)

        commentreplies_serializer = CommentRepliesSerializer(postcomments, many=True)
        return JsonResponse(postreactions_serializer.data, safe=False)
    elif request.method == "PUT":
        commentreplies_data = JSONParser().parse(request)
        commentreplies_serializer = CommentRepliesSerializer(data=commentreplies_data)
        if commentreplies_serializer.is_valid():
            commentreplies_serializer.save()
            return JsonResponse(
                commentreplies_serializer.data, status=status.HTTP_201_CREATED
            )
        return JsonResponse(
            commentreplies_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == "DELETE":
        count = CommentReplies.objects.all().delete()
        return JsonResponse(
            {"message": "{} Comments were deleted successfully!".format(count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )

# get a specific comment reply by ID
@api_view(["GET", "PUT", "DELETE"])
def commentreplies_detail(request, pk):
    # find commentreplies by pk (id)
    try:
        commentreply = CommentReplies.objects.get(pk=pk)
    except PostReactions.DoesNotExist:
        return JsonResponse(
            {"message": "The comment does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    # GET / PUT / DELETE
    if request.method == "GET":
        commentreplies_serializer = CommentRepliesSerializer(commentreply)
        return JsonResponse(commentreplies_serializer.data)

    if request.method == "PUT":
        commentreplies_data = JSONParser().parse(request)
        commentreplies_serializer = CommentRepliesSerializer(
            commentreply, data=commentreplies_data
        )
        if commentreplies_serializer.is_valid():
            commentreplies_serializer.save()
            return JsonResponse(commentreplies_serializer.data)
        return JsonResponse(
            commentreplies_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
