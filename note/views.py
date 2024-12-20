import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import login,authenticate,get_user_model
from django.contrib import messages
from .models import Note
from board.models import Board
from .forms import StickItUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.context import RequestContext
from django.http import JsonResponse,HttpResponse
from board.models import Category
        # notes = Note.objects.all().values('id', 'content', 'border_color', 'coordinates', 'is_finished', 'checkbox_id')
        # print("you went hereeeeeeee")
        # return JsonResponse(list(notes), safe=False)
class NoteView(View):
    def get(self, request, board):
        # TODO PASS THE BOARD NAME HERE!
        try:
            
            # board_obj = Board.objects.get(board_name=board, creator=request.user)
            board_obj = Board.objects.get(board_name=board)
            users_remove = board_obj.users.all().exclude(pk=request.user.id)
            category = Category.objects.all()

            users_add = User.objects.all().exclude(id__in=users_remove).exclude(is_staff=True).exclude(id=request.user.id)
    
        except Board.DoesNotExist:
            return HttpResponse("Board not ig tea found", status=404)
        note_board_name = board  # This will be the name of your board
        print("note: ",note_board_name)
        return render(request, 'note.html',
                       {'note_board_name': note_board_name,
                        "board":board_obj, "add":users_add,
                        "remove":users_remove,
                        "categories":category
                        })
    
# class NoteCreateView(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             print("Furina!")
#             data = json.loads(request.body.decode('utf-8'))
#             content = data.get('content')
#             borderColor = data.get('borderColor')
#             coordinates = data.get('coordinates')
#             is_finished = data.get('is_finished')
#             checkbox_id = data.get('checkbox_id')
#             print(f"Content: {content}, Border Color: {borderColor}, Coordinates: {coordinates}, "
#                 f"is_finished: {is_finished}, checkbox_id: {checkbox_id}")


#             note = Note.objects.create(content=content, border_color=borderColor,coordinates=coordinates,
#                                        is_finished=is_finished, checkbox_id=checkbox_id)

#             print(note.id)
            
#             return JsonResponse({'id': note.id}, status=201)

#         except Exception as e:
#             print(f"Error: {e}")  # Print the error message
#             return JsonResponse({'error': str(e)}, status=400)
        
class NoteUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))

            note = Note.objects.get(pk=pk)
            note_data = serialize_note(note, data)
            print("note data:",note_data)
            return JsonResponse(note_data, status=200)

        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=404)
        except Exception as e:
            print(f"Error: {e}")  # Print the error message
            return JsonResponse({'error': str(e)}, status=400)
        
class NoteDeleteView(View):
    def delete(self, request, pk, *args, **kwargs):
        try:
            note = Note.objects.get(pk=pk)
            note.delete()
            return JsonResponse({'message': 'Note deleted successfully'}, status=200)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
class NoteGetView(View):
    def get(self, request, noteBoardName, *args, **kwargs):
        print("Inside `NoteGetView`")
        try:
            # Fetch the board using the provided name
            board_instance = Board.objects.get(board_name=noteBoardName)
            # Filter notes by this board
            notes = Note.objects.filter(board=board_instance).values(
                'id', 'content', 'border_color', 'coordinates', 'is_finished', 'checkbox_id'
            )
        except Board.DoesNotExist:
            # If the board does not exist, return an empty list or an error
            return JsonResponse({"error": "Board not found"}, status=404)

        return JsonResponse(list(notes), safe=False)

        
        
    
def serialize_note(note, data):
    # Update the note's attributes with the data received
    note.content = data.get('content', note.content)  # Use existing value if key not present
    note.border_color = data.get('border_color', note.border_color)
    note.coordinates = data.get('coordinates', note.coordinates)
    note.is_finished = data.get('is_finished', note.is_finished)
    note.checkbox_id = data.get('checkbox_id', note.checkbox_id)
    # Save the updated note to the database
    note.save()

    # Return the serialized note data
    return {
        'id': note.id,
        'content': note.content,
        'border_color': note.border_color,
        'coordinates': note.coordinates,
        'is_finished': note.is_finished,
        'checkbox_id' : note.checkbox_id
    }      
    

# from django.contrib.auth.views import Temp

# Create your views here.
# PROGRAMMER NAME: AVRIL NIGEL CHUA
class RegisterService(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'register2.html', {'form': StickItUserCreationForm()})
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = StickItUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the error below.')
        return render(request, 'register2.html', {'form': form})
    

class LoginService(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')

class HomeView(View):
    # def get()
    print("welcome home")
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')