import pygame as p
import ChessEngine

width = height = 512
dim = 8
sq_size = height // dim
max_fps = 15
images = {}

#
#Loads Images
#LOAD ONLY ONCE - PREVENT LAG
def loadImages():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png"), (sq_size,sq_size))


def main():
    #starting pygame window
    p.init()
    screen = p.display.set_mode((width,height))
    clock = p.time.Clock() 
    screen.fill(p.Color("white"))

    #loading
    gs = ChessEngine.GameState()
    loadImages()
    
    running = True
    selectedSQs = []
    while running:
        #getting events and acting upon it
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #get location of square which user pressed key
            elif e.type == p.MOUSEBUTTONDOWN:
                locationStart = p.mouse.get_pos()
                colStart = locationStart[0] // sq_size
                rowStart = locationStart[1] // sq_size
                selectedSQs.append((colStart,rowStart))
                print((colStart,rowStart))

            #get location of square which user released key
            elif e.type == p.MOUSEBUTTONUP:
                locationEnd = p.mouse.get_pos()
                colEnd = locationEnd[0] // sq_size
                rowEnd = locationEnd[1] // sq_size
                print((colEnd,rowEnd))

                #checking if released on same square
                if (colEnd,rowEnd) not in selectedSQs:
                    selectedSQs.append((colEnd,rowEnd))
                    print(f"selectedSQs = {selectedSQs}")
                    #checking if it has a start and and end position
                    if len(selectedSQs) == 2:
                        print(selectedSQs[0])
                        print(selectedSQs[1])
                        move = ChessEngine.Move(selectedSQs[0], selectedSQs[1], gs.board)
                        gs.makeMove(move)
                        print(selectedSQs)
                        print(move.getChessNot())
                        selectedSQs = []
                        
                else:
                    selectedSQs = []
                
                
                
            drawGameState(screen, gs)
            clock.tick(max_fps)
            p.display.flip()

def drawBoard(screen, board):
    colors = [p.Color("white"), p.Color("dark gray")]
    for r in range(dim):
        for c in range(dim):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))
    
    
def drawPieces(screen, board):
    for r in range(dim):
        for c in range(dim):
            piece = board[r][c]
            if piece != "  ":
                screen.blit(images[piece], p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))

def drawGameState(screen, gs):
    drawBoard(screen, gs.board)
    drawPieces(screen, gs.board)

if __name__ == "__main__":
    main()

