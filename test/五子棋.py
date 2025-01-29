import numpy as np

# 尝试导入colorama，如果没有安装则使用普通显示
try:
    from colorama import init, Fore, Back, Style
    has_colorama = True
    init()
except ImportError:
    has_colorama = False
    # 创建模拟的Fore和Style类
    class DummyColor:
        def __getattr__(self, name):
            return ''
    Fore = Style = DummyColor()

# 棋型分数
SCORE_FIVE = 100000  # 连五
SCORE_FOUR = 10000   # 活四
SCORE_BLOCKED_FOUR = 1000  # 冲四
SCORE_THREE = 1000   # 活三
SCORE_BLOCKED_THREE = 100  # 眠三
SCORE_TWO = 100      # 活二11
SCORE_BLOCKED_TWO = 10   # 眠二

class GoBang:
    def __init__(self, size=15):
        self.size = size
        self.board = np.array([['+' for _ in range(size)] for _ in range(size)])
        self.current_player = 'X'
        self.search_depth = 4
        
    def print_board(self):
        print('   ' + ' '.join([f'{i+1:2}' for i in range(self.size)]))
        for i in range(self.size):
            print(f'{i+1:2} ', end='')
            for j in range(self.size):
                if self.board[i][j] == 'X':
                    print(f'{Fore.BLACK}X{Style.RESET_ALL} ', end='')
                elif self.board[i][j] == 'O':
                    print(f'{Fore.WHITE}O{Style.RESET_ALL} ', end='')
                else:
                    print('+ ', end='')
            print()

    def get_line_score(self, line, player):
        """评估一条线的分数"""
        score = 0
        length = len(line)
        count = 0
        blocked = 0
        
        for i in range(length):
            if line[i] == player:
                count += 1
            elif line[i] == '+':
                if count >= 5:
                    score += SCORE_FIVE
                elif count == 4:
                    if blocked == 0:
                        score += SCORE_FOUR
                    else:
                        score += SCORE_BLOCKED_FOUR
                elif count == 3:
                    if blocked == 0:
                        score += SCORE_THREE
                    else:
                        score += SCORE_BLOCKED_THREE
                elif count == 2:
                    if blocked == 0:
                        score += SCORE_TWO
                    else:
                        score += SCORE_BLOCKED_TWO
                count = 0
                blocked = 0
            else:
                if count >= 5:
                    score += SCORE_FIVE
                elif count == 4:
                    score += SCORE_BLOCKED_FOUR
                elif count == 3:
                    score += SCORE_BLOCKED_THREE
                elif count == 2:
                    score += SCORE_BLOCKED_TWO
                count = 0
                blocked = 1
        
        # 处理边界情况
        if count >= 5:
            score += SCORE_FIVE
        elif count == 4:
            score += SCORE_BLOCKED_FOUR
        elif count == 3:
            score += SCORE_BLOCKED_THREE
        elif count == 2:
            score += SCORE_BLOCKED_TWO
            
        return score

    def evaluate(self):
        """评估整个棋盘局势"""
        score = {'X': 0, 'O': 0}
        
        # 评估行
        for i in range(self.size):
            score['X'] += self.get_line_score(self.board[i], 'X')
            score['O'] += self.get_line_score(self.board[i], 'O')
        
        # 评估列
        for j in range(self.size):
            score['X'] += self.get_line_score(self.board[:, j], 'X')
            score['O'] += self.get_line_score(self.board[:, j], 'O')
            
        # 评估对角线
        for i in range(self.size-4):
            for j in range(self.size-4):
                score['X'] += self.get_line_score(np.diagonal(self.board[i:i+5, j:j+5]), 'X')
                score['O'] += self.get_line_score(np.diagonal(self.board[i:i+5, j:j+5]), 'O')
                score['X'] += self.get_line_score(np.diagonal(np.fliplr(self.board[i:i+5, j:j+5])), 'X')
                score['O'] += self.get_line_score(np.diagonal(np.fliplr(self.board[i:i+5, j:j+5])), 'O')
                
        return score

    def check_win(self, player):
        """检查是否获胜"""
        # 保持原有的检查逻辑
        for i in range(self.size):
            for j in range(self.size-4):
                if np.all(self.board[i, j:j+5] == player):
                    return True
                
        for j in range(self.size):
            for i in range(self.size-4):
                if np.all(self.board[i:i+5, j] == player):
                    return True
                    
        for i in range(self.size-4):
            for j in range(self.size-4):
                if np.all(np.diagonal(self.board[i:i+5, j:j+5]) == player):
                    return True
                if np.all(np.diagonal(np.fliplr(self.board[i:i+5, j:j+5])) == player):
                    return True
        return False

    def get_valid_moves(self):
        """获取所有可下子位置"""
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == '+':
                    # 只考虑已有棋子周围的位置
                    if self.has_neighbor(i, j):
                        moves.append((i, j))
        return moves

    def has_neighbor(self, x, y, distance=2):
        """检查指定位置周围是否有棋子"""
        for i in range(max(0, x-distance), min(self.size, x+distance+1)):
            for j in range(max(0, y-distance), min(self.size, y+distance+1)):
                if self.board[i][j] != '+':
                    return True
        return False

    def minimax(self, depth, alpha, beta, maximizing_player):
        """极小化极大算法"""
        if depth == 0 or self.check_win('X') or self.check_win('O'):
            scores = self.evaluate()
            return scores['O'] - scores['X']

        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return 0

        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                i, j = move
                self.board[i][j] = 'O'
                eval = self.minimax(depth-1, alpha, beta, False)
                self.board[i][j] = '+'
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                i, j = move
                self.board[i][j] = 'X'
                eval = self.minimax(depth-1, alpha, beta, True)
                self.board[i][j] = '+'
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def computer_move(self):
        """计算机下子"""
        best_score = float('-inf')
        best_move = None
        valid_moves = self.get_valid_moves()
        
        for move in valid_moves:
            i, j = move
            self.board[i][j] = 'O'
            score = self.minimax(self.search_depth, float('-inf'), float('inf'), False)
            self.board[i][j] = '+'
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

def main():
    try:
        if not has_colorama:
            print("提示：安装colorama可以获得更好的显示效果")
            print("可以使用命令：pip install colorama")
        print(f"{Fore.GREEN}欢迎来到五子棋游戏！{Style.RESET_ALL}")
        
        while True:
            try:
                size = int(input("请输入棋盘大小(建议9-19): "))
                if 9 <= size <= 19:
                    break
                print("棋盘大小必须在9-19之间")
            except ValueError:
                print("请输入有效数字")
        
        game = GoBang(size)
        
        while True:
            game.print_board()
            
            # 玩家回合
            while True:
                try:
                    move = input("请输入落子位置(行列，如'1 8'表示第1行第8列，输入'q'退出): ")
                    if move.lower() == 'q':
                        print("\n感谢游玩！再见！")
                        return
                        
                    row, col = map(int, move.split())
                    row -= 1
                    col -= 1
                    if 0 <= row < game.size and 0 <= col < game.size and game.board[row][col] == '+':
                        break
                    print("无效的位置，请重新输入")
                except ValueError:
                    print("输入格式错误，请重新输入")
            
            game.board[row][col] = 'X'
            if game.check_win('X'):
                game.print_board()
                print(f"{Fore.GREEN}恭喜你赢了！{Style.RESET_ALL}")
                break
                
            # 电脑回合
            print("电脑思考中...")
            computer_move = game.computer_move()
            if computer_move:
                row, col = computer_move
                game.board[row][col] = 'O'
                if game.check_win('O'):
                    game.print_board()
                    print(f"{Fore.RED}电脑赢了！{Style.RESET_ALL}")
                    break
            else:
                game.print_board()
                print("平局！")
                break
                
    except KeyboardInterrupt:
        print("\n\n游戏被中断。感谢游玩！再见！")
    except Exception as e:
        print(f"\n发生错误：{e}")
        print("游戏异常退出。")
    finally:
        print("\n游戏结束！")

if __name__ == "__main__":
    main()