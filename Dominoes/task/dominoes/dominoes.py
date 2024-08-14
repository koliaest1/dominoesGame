import random

all_dominoes = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
                [2, 2], [2, 3], [2, 4], [2, 5], [2, 6],
                [3, 3], [3, 4], [3, 5], [3, 6],
                [4, 4], [4, 5], [4, 6],
                [5, 5], [5, 6],
                [6, 6]]


def get_dominoes(dominoes):
    user_dominoes = []
    computer_dominoes = []
    stock_pieces = dominoes
    for i in range(0, 7):
        domino = stock_pieces[random.randint(0, len(stock_pieces) - 1)]
        user_dominoes.append(domino)
        stock_pieces.remove(domino)
    for i in range(0, 7):
        domino = stock_pieces[random.randint(0, len(stock_pieces) - 1)]
        computer_dominoes.append(domino)
        stock_pieces.remove(domino)
    return user_dominoes, computer_dominoes, stock_pieces


def starting_pieces(dominoes):
    while True:
        user_dominoes, computer_dominoes, stock_pieces = get_dominoes(dominoes)
        user_max = max([piece for piece in user_dominoes if piece[0] == piece[1]], default=[])
        comp_max = max([piece for piece in computer_dominoes if piece[0] == piece[1]], default=[])

        if user_max or comp_max:
            if user_max > comp_max:
                user_dominoes.remove(user_max)
                snake = [user_max]
                return stock_pieces, user_dominoes, computer_dominoes, snake, 'computer'
            else:
                computer_dominoes.remove(comp_max)
                snake = [comp_max]
                return stock_pieces, user_dominoes, computer_dominoes, snake, 'player'


def user_turn(user_dominoes, stock_dominoes, snake):
    while True:
        try:
            user_choice = int(input())
            if abs(user_choice) > len(user_dominoes):
                print('Invalid input. Please try again.')
                continue

            if user_choice == 0:
                if stock_dominoes:
                    pick = stock_dominoes.pop(random.randint(0, len(stock_dominoes) - 1))
                    user_dominoes.append(pick)
                else:
                    print("Stock is empty. You must play.")
                return user_dominoes, stock_dominoes, snake, 'computer'

            piece = user_dominoes[abs(user_choice) - 1]

            if user_choice < 0 and legal_move(snake[0], piece):
                legal_piece = make_legal_move(snake[0], piece, at_start=True)
                if legal_piece is not None:
                    snake.insert(0, legal_piece)
                    user_dominoes.remove(piece)
                    return user_dominoes, stock_dominoes, snake, 'computer'
            elif user_choice > 0 and legal_move(snake[-1], piece):
                legal_piece = make_legal_move(snake[-1], piece)
                if legal_piece is not None:
                    snake.append(legal_piece)
                    user_dominoes.remove(piece)
                    return user_dominoes, stock_dominoes, snake, 'computer'
            else:
                print('Illegal move. Please try again.')
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")


def computer_turn(computer_dominoes, stock_dominoes, snake):
    while True:
        if len(computer_dominoes) == 0:
            print('Status: The game is over. The computer won!')
            break
        else:
            user_choice = input()  # Wait for the user to press Enter
            next_user = 'player'

            if user_choice == "":
                move_made = False

                for i in range(len(computer_dominoes)):
                    pick = computer_dominoes[i]

                    # Try to place at the start of the snake
                    piece = make_legal_move(snake[0], pick, at_start=True)
                    if piece is not None:
                        snake.insert(0, piece)
                        computer_dominoes.remove(pick)
                        move_made = True
                        break

                    # Try to place at the end of the snake
                    piece = make_legal_move(snake[-1], pick)
                    if piece is not None:
                        snake.append(piece)
                        computer_dominoes.remove(pick)
                        move_made = True
                        break

                # Check for any issue with None being added
                if not move_made:
                    if stock_dominoes:
                        pick = stock_dominoes.pop(random.randint(0, len(stock_dominoes) - 1))
                        computer_dominoes.append(pick)
                else:
                    # Sanity check to ensure no None is in the snake
                    if None in snake:
                        print("Error: None was added to the snake!")
                        print("Snake:", snake)
                        return computer_dominoes, stock_dominoes, snake, next_user

                break
            else:
                print('Invalid input. Please try again.')
                continue

    return computer_dominoes, stock_dominoes, snake, next_user


def playing_field(stock_pieces, user_dominoes, computer_dominoes, snake):
    print("=" * 70)
    print(f'Stock size: {len(stock_pieces)}')
    print(f'Computer pieces: {len(computer_dominoes)}')
    print()
    if len(snake) <= 6:
        print(*snake, sep="")
    else:
        print(*snake[0:3], "...", *snake[-3:])
    print()
    print(f'Your pieces:')
    for i in range(len(user_dominoes)):
        print(f'{i + 1}:{user_dominoes[i]}')
    print()


def make_legal_move(position, domino, at_start=False):
    """
    Adjusts the domino to match the given position.
    If at_start is True, it matches position[0] to the domino.
    Otherwise, it matches position[1] to the domino.
    """
    if at_start:
        if position[0] == domino[1]:
            return domino  # Already matches correctly
        elif position[0] == domino[0]:
            return [domino[1], domino[0]]  # Needs to be flipped to match
    else:
        if position[1] == domino[0]:
            return domino  # Already matches correctly
        elif position[1] == domino[1]:
            return [domino[1], domino[0]]  # Needs to be flipped to match

    # Explicitly return None if no valid move can be made
    return None


def legal_move(position, domino):
    return position[0] in domino or position[1] in domino


def evaluate_dominoes(computer_dominoes, stock_dominoes):
    rating = {}
    for i in range(0, 7):
        count = 0
        for domino in computer_dominoes:
            if i in domino and domino[0] != domino[1]:
                count += 1
            elif i in domino and domino[0] == domino[1]:
                count += 2
        for domino in stock_dominoes:
            if i in domino and domino[0] != domino[1]:
                count += 1
            elif i in domino and domino[0] == domino[1]:
                count += 2
        rating[i] = count
    return rating


def count_domino_scores(computer_dominoes, stock_dominoes):
    ratings = evaluate_dominoes(computer_dominoes, stock_dominoes)
    rated_dict = {}
    sorted_rating = {}
    for domino in computer_dominoes:
        score = ratings[domino[0]] + ratings[domino[1]]
        dom_tuple = (domino[0], domino[1])
        rated_dict[dom_tuple] = score
    sorted_rating = sorted(rated_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_rating


def draw(snake):
    first_end = snake[0][0]
    last_end = snake[-1][1]

    # Check if the ends are the same
    if first_end != last_end:
        return False

    count = 0
    for domino in snake:
        count += domino.count(first_end)

    # If the count reaches 8, it means all possible dominoes with this number have been played
    return count == 8


def main():
    stock_pieces, user_pieces, computer_pieces, snake, turn = starting_pieces(all_dominoes)
    playing_field(stock_pieces, user_pieces, computer_pieces, snake)
    while True:
        if len(user_pieces) == 0:
            print('Status: The game is over. You won!')
            break
        elif len(computer_pieces) == 0:
            print('Status: The game is over. The computer won!')
            break
        elif draw(snake):
            print('Status: The game is over. It\'s a draw!')
            break
        else:
            if turn == "player":
                print("Status: It's your turn to make a move. Enter your command.")
                user_pieces, stock_pieces, snake, turn = user_turn(user_pieces, stock_pieces, snake)
                playing_field(stock_pieces, user_pieces, computer_pieces, snake)
                continue
            else:
                print("Status: Computer is about to make a move. Press Enter to continue...")
                computer_pieces, stock_pieces, snake, turn = computer_turn(computer_pieces, stock_pieces, snake)
                playing_field(stock_pieces, user_pieces, computer_pieces, snake)
                continue


if __name__ == "__main__":
    main()
