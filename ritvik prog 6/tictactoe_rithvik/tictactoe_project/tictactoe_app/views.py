from django.shortcuts import render
from django.http import JsonResponse
import json

game_state = {
    'grid': {},
    'turn': 'X',
    'status': 'P',
}

def x(request):
    return render(request, 'tictactoe_app/x.html')

def o(request):
    return render(request, 'tictactoe_app/o.html')

def game(request):
    global game_state
    if request.method == 'POST':
        data = json.loads(request.body)
        move = data.get('move', None)
        if move:
            game_state['grid'][f'g{move[0]}{move[1]}'] = game_state['turn']
            # Check for game over conditions and update the game state
            game_state = check_game_over(game_state)
            game_state['turn'] = 'O' if game_state['turn'] == 'X' else 'X'
    return JsonResponse(game_state)

def check_game_over(game_state):
    # Add your logic to check if the game is over (win/draw)
    # Update the 'status' field in the game_state dictionary accordingly
    return game_state
