CC= g++
OBJ_LIST= draw.o
SRC_PATH= src/
OBJ_PATH= obj/

CPPFLAGS_COMMON= -Wall -O3 -std=c++11
CPPFLAGS_RELEASE= $(CPPFLAGS_COMMON) -DNDEBUG
CPPFLAGS_DEBUG= $(CPPFLAGS_COMMON)
TARGET= draw

OBJS= $(addprefix $(OBJ_PATH), $(OBJ_LIST))

.PHONY: all debug compile clean

all: CPPFLAGS=$(CPPFLAGS_RELEASE)
all: compile

debug: CPPFLAGS=$(CPPFLAGS_DEBUG) 
debug: compile

compile: obj clean $(OBJS)
	$(CC) -o $(TARGET) $(OBJS) $(CPPFLAGS)

obj:
	-mkdir -p $(OBJ_PATH)

$(OBJ_PATH)%.o: $(SRC_PATH)%.cpp
	$(CC) -c -o $@ $< $(CPPFLAGS)

clean:
	-rm $(TARGET)
	-rm $(OBJ_PATH)*
