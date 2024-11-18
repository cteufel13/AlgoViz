import pygame


class Button:
    def __init__(self, relative_pos, name, font_size=36):
        self.relative_pos = relative_pos
        self.name = name
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.text = self.font.render(name, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=relative_pos)
        self.border_thickness = 2
        self.is_active = False

    def draw(self, screen):
        # Draw the button with a border if active
        border_color = (0, 255, 0) if self.is_active else (255, 255, 255)
        pygame.draw.rect(screen, border_color, self.text_rect.inflate(self.border_thickness * 4, self.border_thickness * 4), self.border_thickness)
        screen.blit(self.text, self.text_rect)

    def updatePosition(self, screen_size):
        # Update the button's absolute position based on the screen size
        abs_x = int(screen_size[0] * self.relative_pos[0])
        abs_y = int(screen_size[1] * self.relative_pos[1])
        self.text_rect = self.text.get_rect(center=(abs_x, abs_y))

    def is_hovered(self, mouse_pos):
        return self.text_rect.collidepoint(mouse_pos)

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

class ShapeButton:
    def __init__ (self,relative_pos,name,screen,shape_params,drawfunction):
        self.relative_pos = relative_pos
        self.name = name
        self.screen = screen
        self.params = shape_params
        self.drawfunction = drawfunction
        self.is_active = False
        self.shape = None
        self.color = (255,255,255)

    def draw(self):
        pass 

    def is_hovered(self, mouse_pos):
        return self.shape.collidepoint(mouse_pos)

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

class CircleButton(ShapeButton):
    def __init__ (self,relative_pos,name,screen,shape_params,drawfunction):
        super().__init__(relative_pos,name,screen,shape_params,drawfunction)
    
    def draw(self,screen_size=None):
        if screen_size== None:
            screen_size = self.screen.get_size()
        self.shape = self.drawfunction(self.screen,self.color,(self.relative_pos[0]*screen_size[0],self.relative_pos[1]*screen_size[1]),self.params*screen_size[0])

class SquareButton(ShapeButton):
    def __init__(self, relative_pos, name, screen, shape_params, drawfunction):
        super().__init__(relative_pos, name, screen, shape_params, drawfunction)

    def draw(self,screen_size=None):
        

        if screen_size ==None:
            screen_size = self.screen.get_size()
        
        self.shape = self.drawfunction(self.screen,self.color,(self.relative_pos[0]*screen_size[0]-self.params*screen_size[0],self.relative_pos[1]*screen_size[1]-self.params*screen_size[0],2*self.params*screen_size[0],2*self.params*screen_size[0]))


class TextBox():
    def __init__ (self, name:str,type:type,relative_pos,box_size,maxval,defaulttext):
        self.relative_pos = relative_pos
        self.box_size = box_size
        self.name = name
        self.type = type
        self.text = ""
        self.defaulttext = defaulttext
        self.value = -1
        self.fontsize = 42
        self.font = pygame.font.Font(None, self.fontsize)
        self.active = False
        self.cursor_visible = False  # Cursor visibility for blinking effect
        self.cursor_position = 0
        self.cursor_blink_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.cursor_blink_event, 500)
        self.maxval = maxval


    def handleMouseDown(self,event,screen):
        size = screen.get_size()

        rect = pygame.Rect(self.relative_pos[0]*size[0], self.relative_pos[1]*size[1], self.box_size[0]*size[0], self.box_size[1]*size[1])
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state based on mouse position
            if rect.collidepoint(event.pos):
                self.active = True
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            else:
                self.active = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    def handleKeyPress(self,event,screen):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(f"Entered text: {self.text}")
                self.text = ""  # Clear text on Enter
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                self.cursor_position = max(0, self.cursor_position - 1)
            elif event.key == pygame.K_LEFT:
                self.cursor_position = max(0, self.cursor_position - 1)
            elif event.key == pygame.K_RIGHT:
                self.cursor_position = min(len(self.text), self.cursor_position + 1)
            else:
                if event.unicode.isdigit():  # Check if the character is a digit
                    print('Char is Digit')
                    new_text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                    print(new_text)
                    if int(new_text) <= self.maxval:  # Check if the new number is within the allowed range
                        self.text = new_text
                        self.value = int(new_text)
                        self.cursor_position += 1
            
    
    def handleMouseMotion(self,event,screen):
        size = screen.get_size()
        rect = pygame.Rect(self.relative_pos[0]*size[0], self.relative_pos[1]*size[1], self.box_size[0]*size[0], self.box_size[1]*size[1])
        self.fontsize = size[0]//45
        self.font = pygame.font.Font(None, self.fontsize) 
        if event.type == pygame.MOUSEMOTION:
            # Change cursor based on hover status
            if rect.collidepoint(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif event.type == self.cursor_blink_event and self.active:
            # Toggle cursor visibility
            self.cursor_visible = not self.cursor_visible
            
    def draw(self,screen):
        size = screen.get_size()

        rect = pygame.Rect(self.relative_pos[0]*size[0], self.relative_pos[1]*size[1], self.box_size[0]*size[0], self.box_size[1]*size[1])
        self.fontsize = size[0]//45
        self.font = pygame.font.Font(None, self.fontsize)
        pygame.draw.rect(screen,(175,175,175) if self.active else (255,255,255),rect,2)
        if self.text == "":
            text = self.font.render(self.defaulttext,True,(120,120,120))
        else:
            text = self.font.render(self.text,True,(255,255,255))
        screen.blit(text, (rect.x + 5, rect.y + (rect.height - text.get_height()) // 2))

        if self.active and self.cursor_visible:
            cursor_x = rect.x + 5 + self.font.size(self.text[:self.cursor_position])[0]
            cursor_y = rect.y + 5
            cursor_height = self.font.size(self.text)[1]
            pygame.draw.line(screen, (0,0,0), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)



def generateColorGradient(length):
    gradientcolors = []
    start_color =(230, 230, 250)
    end_color = (48, 25, 52)

    for i in range(length):
        t = i/(length -1)
        r= round((1-t)* start_color[0] + t* end_color[0],1)
        g= round((1-t)* start_color[1] + t* end_color[1],1)
        b= round((1-t)* start_color[2] + t* end_color[2] ,1)

        gradientcolors.append((r,g,b))  

    return gradientcolors

    