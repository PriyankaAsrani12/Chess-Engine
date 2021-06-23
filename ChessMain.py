import pygame as p
from ChessEngine import ChessEngineFile

WIDTH=HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImage():
    pieces=["bp", "bR", "bN", "bB", "bQ", "bK", "wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece]=p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))

def main():
    p.init()
    screen=p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=ChessEngineFile.GameState()
    validMoves=gs.getValidMoves()
    moveMade=False

    loadImage()
    running=True
    sqSelected=()
    playerClicks=[]
    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()
                col=location[0]//SQ_SIZE
                row=location[1]//SQ_SIZE
                if sqSelected==(row,col):
                    sqSelected=()
                    playerClicks=[]
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks)==2:
                    move=ChessEngineFile.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade=True
                    sqSelected=()
                    playerClicks=[]
            elif e.type==p.KEYDOWN:
                if e.key==p.K_z:
                    gs.undoMove()
                    moveMade=True
        if moveMade:
            validMoves=gs.getValidMoves()
            moveMade=False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawBoard(screen):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if (row+col)%2==0:
                p.draw.rect(screen,p.Color("white"),p.Rect(col * SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                p.draw.rect(screen, p.Color("grey"), p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen,board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece=board[row][col]
            if piece!="--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

if __name__=="__main__":
    main()