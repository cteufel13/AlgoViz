import pygame
import sys
import numpy as np
import time
from src.visualisation.vis_utils import Button, CircleButton,SquareButton,TextBox
from src.visualisation.vis_utils import generateColorGradient
import math

class Visualiser:
    def __init__(self, algorithms, gridshape: tuple):
        pygame.init()
        self.algorithms = algorithms
        self.algorithm = algorithms[0]
        self.gridshape = gridshape
        self.width = 1000
        self.height = 750
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Algorithms Visualiser")

        # Initialize variables
        self.squares = []
        self.square_colors = [(255, 255, 255) for _ in range(gridshape[0] * gridshape[1])]  # Initialize to white
        self.count = 0
        self.BoolStartEnd = False
        self.grid = np.ones(gridshape[0] * gridshape[1])

        # Create the initial grid layout
        self.updateGridLayout()

        self.mouse_button_down = False

        self.optimal_path = []
        self.pointsvisited = []
        self.pointsprinted = [] 


        # Line drawing mode variables
        self.line_mode = False
        self.line_start = None
        self.line_end = None

        self.draw_shape_mode = False
        self.draw_shape_type = 0

        self.setstartstop_mode = False
        self.count = 0

        self.mode = 0
        

        self.size = 4
        self.value = 3
        self.maxcost = 10

        colors = [(255,255,255)]
        colors.extend(generateColorGradient(self.maxcost))
        colors.append((255,0,0))
        self.gradientcolor = colors

        self.runningalgo = False
        

        self.buttons = {
            "Set Start/End": Button(relative_pos=(0.1, 0.5), name="Set Start/End"),
            "Run": Button(relative_pos=(0.1, 0.4), name="Run"),
            "Draw Line": Button(relative_pos=(0.9, 0.5), name="Draw Line"),
            "Draw Shape": Button(relative_pos=(0.9, 0.6), name="Draw Shape"), 
            "Reset": Button(relative_pos=(0.1, 0.6), name="Reset"),
            "Clear": Button(relative_pos=(0.1, 0.7), name="Clear"),
            ">": Button(relative_pos=(0.6, 0.05), name=">"),
            "<": Button(relative_pos=(0.4, 0.05), name="<")
        }

        self.shapebutton = {
            "Circle": CircleButton(relative_pos=(0.875,0.7),name='Circle',screen=self.screen,shape_params=(0.02),drawfunction=pygame.draw.circle),
            "Square": SquareButton(relative_pos=(0.925,0.7),name="Square",screen=self.screen,shape_params=(0.02),drawfunction=pygame.draw.rect)
        }
        
        self.textbox = {
            "Size": TextBox(name='Size',type=int,relative_pos=(0.875,0.8),box_size=(0.05,0.03),maxval = max(gridshape[0],gridshape[1])//2,defaulttext='Size'),
            "Value": TextBox(name='Value',type=int,relative_pos=(0.875,0.85),box_size=(0.05,0.03),maxval = self.maxcost,defaulttext='Value')
        }


        self.run()

    def showGrid(self):
        # Draw each square with its current color
        for i in range(len(self.squares)):
            pygame.draw.rect(self.screen, self.square_colors[i], self.squares[i])

    def updateGridLayout(self):
        # Recalculate square sizes and positions based on the window size
        screen_width, screen_height = self.screen.get_size()
        n, m = self.gridshape
        square_size = min(screen_width // n, screen_height // m) * 0.7
        gap = square_size // 10

        # Calculate starting position to center the grid
        x_start, y_start = self.get_grid_start_position(screen_width, screen_height, n, m, square_size, gap)

        self.squares.clear()

        # Calculate positions and store them in self.squares
        for row in range(m):
            for col in range(n):
                x = x_start + col * (square_size + gap * 2)
                y = y_start + row * (square_size + gap * 2)
                rect = pygame.Rect(x, y, square_size, square_size)
                self.squares.append(rect)

    def updateButtonPositions(self):
        # Update button positions based on the window size
        screen_size = self.screen.get_size()
        for button in self.buttons.values():
            button.updatePosition(screen_size)
        for button in self.shapebutton.values():
            button.draw(screen_size)
                
    def drawTitle(self):
        font = pygame.font.Font(None, 52)
        text = font.render(f'{self.algorithm}', True, (255, 255, 255))
        text_rect = text.get_rect(center=(0.5*self.width, 0.05*self.height))
        self.screen.blit(text, text_rect)

    def drawLine(self):
        # Draw a line by making squares red between self.line_start and self.line_end
        if self.line_start is not None and self.line_end is not None:
            start_row, start_col = divmod(self.line_start, self.gridshape[0])
            print(self.line_start,self.gridshape[0])
            end_row, end_col = divmod(self.line_end, self.gridshape[0])
            
            # Use Bresenham's line algorithm to get points on the line
            line_points = self.getGridLine(start_row, start_col, end_row, end_col)
            
            # Set each square in the line to red
            for row, col in line_points:
                index = row * self.gridshape[0] + col
                if 0 <= index < len(self.square_colors):  # Ensure it's within bounds
                    current_color = self.gradientcolor[self.value]
                    self.square_colors[index] = (255, 255, 255) if self.square_colors[index] == current_color else current_color
                    self.grid[index] = 1 if self.grid[index] == self.value else self.value
            
            # Reset line points after drawing
            self.line_start, self.line_end = None, None


    def handleSquareClick(self, event):
    # Handle square click behavior
        if not self.BoolStartEnd:
            for index, square in enumerate(self.squares):
                if square.collidepoint(event.pos):
                    # Toggle color between self.value's color and white
                    current_color = self.gradientcolor[self.value]
                    self.square_colors[index] = (255, 255, 255) if self.square_colors[index] == current_color else current_color
                    self.grid[index] = 1 if self.grid[index] == self.value else self.value
                    break
        else:
            for index, square in enumerate(self.squares):
                
                if square.collidepoint(event.pos):
                    # Toggle color between green and white for start/end
                    self.square_colors[index] = (0, 255, 0) if self.square_colors[index] == (255, 255, 255) else (255, 255, 255)
                    if self.count == 3:
                        for index2, square in enumerate(self.squares):
                            if self.square_colors[index2] == (0,255,0):
                                self.square_colors[index2] = (255,255,255)
                                self.grid[index2] = 1
                        self.count = 2
                        self.grid[index] = -2  # Start
                        self.square_colors[index] = (0,255,0)
                        break
                    if self.count == 1:
                        self.count = 2
                        self.grid[index] = -2  
                        break
                    if self.count == 2:
                        self.count = 3
                        self.grid[index] = -3  # End
                    
                    break

    def handleTextboxClick(self,event):
        for name,box in self.textbox.items():
            box.handleMouseDown(event,self.screen)
        
    def handleTextboxKey(self,event):
        for name,box in self.textbox.items():
            box.handleKeyPress(event,self.screen)
    
    def handleTexboxMotion(self,event):
        for name,box in self.textbox.items():
            box.handleMouseMotion(event,self.screen)
            
    def handleButtonActions(self, event):
        for name, button in self.buttons.items():
            if button.is_hovered(event.pos):
                
                
                if name == "Set Start/End":
                    self.setstartstop_mode = not self.setstartstop_mode
                    self.BoolStartEnd = True
                    self.count = 1

                    if self.setstartstop_mode:
                        button.activate()
                    else:
                        button.deactivate()
                    self.mode = next(i for i, (key, value) in enumerate(self.buttons.items()) if value.name == name)
                    break
                elif name == "Run":
                    self.runAlgorithm()
                    self.mode = next(i for i, (key, value) in enumerate(self.buttons.items()) if value.name == name)
                    break
                elif name == "Draw Line":
                    self.line_mode = not self.line_mode
                    if self.line_mode:
                        button.activate()
                    else:
                        button.deactivate()
                    self.line_start, self.line_end = None, None
                    self.mode = next(i for i, (key, value) in enumerate(self.buttons.items()) if value.name == name)
                    break
                elif name == "Draw Shape":
                    self.draw_shape_mode = not self.draw_shape_mode
                    if self.draw_shape_mode:
                        button.activate()
                    else:
                        button.deactivate()
                    self.mode = next(i for i, (key, value) in enumerate(self.buttons.items()) if value.name == name)
                    break
                elif name == "Reset":
                    
                    for i in range(len(self.square_colors)):
                        if self.square_colors[i] not in self.gradientcolor:
                            self.square_colors[i] = (255, 255, 255)
                            self.grid[i] = 1
                    self.mode = next(i for i, (key, value) in enumerate(self.buttons.items()) if value.name == name)
                    break
                elif name == "Clear":
                    for i in range(len(self.square_colors)):
                        self.square_colors[i] = (255, 255, 255)
                        self.grid[i] = 1
                    self.optimal_path = []
                    self.pointsvisited = []
                    self.pointsprinted = []
                    self.runningalgo = False
                    self.mode = next(i for i, (key, value) in enumerate(self.buttons.items()) if value.name == name)
                    break
                elif name == ">":
                    self.algorithm = self.algorithms[(self.algorithms.index(self.algorithm) + 1) % len(self.algorithms)]
                    self.mode = next(i for i, (key, value) in enumerate(self.buttons.items()) if value.name == name)
                    break
                elif name == "<":
                    self.algorithm = self.algorithms[(self.algorithms.index(self.algorithm) - 1) % len(self.algorithms)]
                    self.mode = next(i for i, (key, value) in enumerate(self.buttons.items()) if value.name == name)
                
            
    def handleShapeButtonClick(self,pos):
        for name, button in self.shapebutton.items():
            if button.is_hovered(pos):
                if name == 'Square':
                    self.draw_shape_type = 2
                    return
                if name == 'Circle':
                    self.draw_shape_type = 1
                    return
        for index, square in enumerate(self.squares):
            if square.collidepoint(pos):
                if self.draw_shape_type ==1:
                    self.drawShape(index)
                    return
                elif self.draw_shape_type == 2:
                    self.drawShape(index)
                    return
        
        self.draw_shape_type = 0


        
            
    def drawShape(self,pos):
        if self.draw_shape_type == 1:
            self.drawCircle(pos)
        if self.draw_shape_type ==2:
            self.drawSquare(pos)
        

    def drawCircle(self,pos):
        # Draw a circle by making squares red within a radius from center
            if pos is not None:
                center_row, center_col = divmod(pos, self.gridshape[0])
                
                # Get all points within the radius
                circle_points = self.getCirclePoints(center_row, center_col, self.size)
                
                # Set each square in the circle to red
                for row, col in circle_points:
                    if 0 <= row < self.gridshape[0] and 0 <= col < self.gridshape[1]:  # Check bounds
                        index = row * self.gridshape[1] + col
                        self.square_colors[index] = self.gradientcolor[self.value]  # Set color to red
                        self.grid[index] = self.value  # Mark this point as highlighted
            
    def getCirclePoints(self, center_row, center_col, radius):
    # This function calculates all points within a circular radius around a center point
        points = []
        for row in range(center_row - radius, center_row + radius + 1):
            for col in range(center_col - radius, center_col + radius + 1):
                # Calculate the distance to the center
                distance = math.sqrt((center_row - row) ** 2 + (center_col - col) ** 2)
                if distance <= radius:
                    points.append((row, col))
        return points
    
    def drawSquare(self, pos):
        # Draw a square by making squares red within a side length from center
        if pos is not None:
            center_row, center_col = divmod(pos, self.gridshape[0])
            
            # Calculate the range for the square area
            half_side = self.size
            square_points = self.getSquarePoints(center_row, center_col, half_side)
            
            # Set each square in the area to red
            for row, col in square_points:
                if 0 <= row < self.gridshape[0] and 0 <= col < self.gridshape[1]:  # Ensure within bounds
                    index = row * self.gridshape[1] + col
                    self.square_colors[index] = self.gradientcolor[self.value]  # Set color to red
                    self.grid[index] = self.value  # Mark this point as highlighted

    def getSquarePoints(self, center_row, center_col, half_side):
        # Calculate all points within the square area
        points = []
        for row in range(center_row - half_side, center_row + half_side + 1):
            for col in range(center_col - half_side, center_col + half_side + 1):
                points.append((row, col))
        return points

    def handleLineClick(self, pos):
        # Handle line-drawing clicks
        for index, square in enumerate(self.squares):
            if square.collidepoint(pos):
                if self.line_start is None:
                    self.line_start = index
                elif self.line_end is None:
                    self.line_end = index
                    self.drawLine()
                break

    @staticmethod
    def get_grid_start_position(screen_width, screen_height, n, m, square_size, gap=0):
        grid_width = m * square_size +(m-1)*gap*2
        grid_height = n * square_size +(n-1)*gap*2
        x_start = (screen_width - grid_width) // 2
        y_start = (screen_height - grid_height) // 2
        return x_start, y_start
    
    def runAlgorithm(self):
        grid = self.grid.reshape(self.gridshape)
        self.algorithm.start = tuple(int(arr[0]) for arr in np.where(grid == -2))
        self.algorithm.end = tuple(int(arr[0]) for arr in np.where(grid == -3))
        grid[grid == -2] = 1
        grid[grid == -3] = 1
        self.algorithm.map = grid 
        self.optimal_path,self.pointsvisited = self.algorithm.run_algorithm()
        self.pointsprinted.append(self.optimal_path.pop(0))
        self.runningalgo = True
        print('Done Running')

    def getGridLine(self, x0, y0, x1, y1):
        points = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            points.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return points
    
    def run(self):
        while True:
            # Fill the screen background and display elements
            self.screen.fill((30, 30, 30))
            self.showGrid()  # Only redraw the squares based on updated colors
            self.drawTitle()
            default_cursor = pygame.SYSTEM_CURSOR_ARROW  # Default arrow cursor
            hover_cursor = pygame.SYSTEM_CURSOR_HAND
            if self.textbox['Value'].text == "":
                self.value = -1
            else: self.value = self.textbox['Value'].value

            if self.textbox['Size'].text == "":
                self.size = 1
            else:
                self.size = self.textbox['Size'].value

            
            # Draw buttons
            self.width, self.height = self.screen.get_size()
            for button in self.buttons.values():
                button.draw(self.screen)
            
            for name, button in self.shapebutton.items():
                if name == 'Circle' and self.draw_shape_type == 1:
                    button.color = (125,125,125)
                elif name == 'Square' and self.draw_shape_type == 2:
                    button.color = (125,125,125)
                else:
                    button.color = (255,255,255)
                button.draw()

            for textbox in self.textbox.values():
                    textbox.draw(screen=self.screen)

            #Hover Check:
            for button in self.buttons.values():
                if button.is_hovered(pygame.mouse.get_pos()):
                    pygame.mouse.set_cursor(hover_cursor)
                    break
                else:
                    pygame.mouse.set_cursor(default_cursor)
            
            for button in self.shapebutton.values():
                if button.is_hovered(pygame.mouse.get_pos()) or button.is_active :
                    pygame.mouse.set_cursor(hover_cursor)
                    button.color = (125,125,125)
                    break
                else:
                    pygame.mouse.set_cursor(default_cursor)
                    button.color = (255,255,255)

            for button in self.buttons.values():
                if self.mode != next(i for i, (key, value) in enumerate(self.buttons.items()) if value.name == button.name):
                    if button.name == "Set Start/End":
                        if self.BoolStartEnd:
                            self.grid[self.grid == -2] = 1
                            self.square_colors = [(255,255,255) if x == (0,255,0) else x for x in self.square_colors]
                            self.grid[self.grid == -3] = 1
                            button.deactivate()
                            self.BoolStartEnd = False
                    
                    if button.name == "Draw Line":
                        self.line_mode = False
                        button.deactivate()
                    
                    if button.name == "Draw Shape":
                        button.deactivate()
                            

            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.size
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                    self.updateGridLayout()  # Only update layout, not colors
                    self.updateButtonPositions()
                
                elif event.type == pygame.MOUSEBUTTONDOWN and self.runningalgo == False:
                    self.handleButtonActions(event)
                    self.handleTextboxClick(event)
                    if self.line_mode:
                        self.handleSquareClick(event)
                        self.handleLineClick(event.pos)
                    elif self.draw_shape_mode:
                        self.handleShapeButtonClick(event.pos)
                    else:
                        self.handleSquareClick(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.handleTexboxMotion(event)
                elif event.type == pygame.KEYDOWN:
                    self.handleTextboxKey(event)
            if self.runningalgo:
                if not self.pointsvisited and not self.optimal_path:
                    self.runningalgo = False
                elif self.pointsvisited:
                    if not self.pointsvisited[next(iter(self.pointsvisited))] :
                        point = next(iter(self.pointsvisited))
                        self.pointsvisited.pop(point)
                        self.square_colors[point[0] * self.gridshape[0] + point[1]] = (0, 0, 255)
                        self.pointsprinted.append(point)
                    else:
                        point = self.pointsvisited[next(iter(self.pointsvisited))].pop(0)
                        if self.square_colors[point[0] * self.gridshape[0] + point[1]] == (255, 255, 255):
                            self.square_colors[point[0] * self.gridshape[0] + point[1]] = (0, 0, 125)
                            self.pointsprinted.append(point)

                elif self.optimal_path:
                    point = self.optimal_path.pop(0)
                    self.square_colors[point[0] * self.gridshape[0] + point[1]] = (0, 255, 0)
                    self.pointsprinted.append(point)
                    time.sleep(0.1)
                    
            # Update the display
            pygame.display.flip()