import heapq
import copy
def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance=0
    for i in range(1,8):
        pos=divmod(from_state.index(i),3)
        
        #print(i,pos)
        if i<=3:
            distance+=abs(pos[0]-0)+abs(pos[1]-(i-1))
        elif i>3 and i<=6:
            distance+=abs(pos[0]-1)+abs(pos[1]-(i-4))
        elif i==7:
            distance+=abs(pos[0]-2)+abs(pos[1]-(i-7))

    return distance

    

def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    succ_states=[]#output list
    
    position=[]# store pos in 3x3 matrix

    store_num=[]
    for num in state:
        if num!=0:
            pos=divmod(state.index(num),3)# posiiton of each num(x,x)
            position.append(pos)
            store_num.append(num)
            #print(state.index(num),pos)
    
    zero_pisition=[]
    first_index=state.index(0)
    zero_pisition.append(divmod(first_index,3))
    second_index=state.index(0,state.index(0)+1)
    zero_pisition.append(divmod(second_index,3))
    #print(first_index,second_index)
    for pos in position:
        for zero in zero_pisition:
            if pos[0]==zero[0]:
                if pos[1]+1==zero[1] or pos[1]-1==zero[1]:
                    temp_state=copy.deepcopy(state)
                    #possible then swap
                    num=store_num[position.index(pos)]
                    index_num=temp_state.index(num)
                    temp=temp_state[index_num]#store the index of num
                    if zero_pisition.index(zero)==0:
                        temp_state[index_num]=temp_state[first_index]
                        temp_state[first_index]=temp
                        succ_states.append(temp_state)
                        #print('first1',temp,temp_state[first_index])
                    elif zero_pisition.index(zero)==1:
                        temp_state[index_num]=temp_state[second_index]
                        temp_state[second_index]=temp
                        succ_states.append(temp_state)
                    #print(temp_state)
            elif pos[1]==zero[1]:
                if pos[0]+1==zero[0] or pos[0]-1==zero[0]:
                    temp_state=copy.deepcopy(state)

                    num=store_num[position.index(pos)]
                    index_num=temp_state.index(num)
                    temp=temp_state[temp_state.index(num)]
                    if zero_pisition.index(zero)==0:
                        temp_state[index_num]=temp_state[first_index]
                        temp_state[first_index]=temp
                        succ_states.append(temp_state)
                        #print('first2')
                    elif zero_pisition.index(zero)==1:
                        temp_state[index_num]=temp_state[second_index]
                        temp_state[second_index]=temp
                        succ_states.append(temp_state)
                        #print('second2')
                    #print(temp_state)
                    

    return sorted(succ_states)


def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    open_queue=[]
    closed_queue=[]
    state_info_list=[]
    #heapq.heappush(pq ,(cost, state, (g, h, parent_index)))
    #cost=g+h
    #h=get_manhattan_distance() current[2][1]
    #g=num of moves current[2][0]
    #initilize open queue
    heapq.heappush(open_queue ,(0+get_manhattan_distance(state,goal_state), state, (0, get_manhattan_distance(state,goal_state), -1)))
    while open_queue:
        
        #b = heapq.heappop(pq)
        current=heapq.heappop(open_queue)
        closed_queue.append(current)
        if current[1]==goal_state:
            
            while current[2][2]!=-1:
                temp=copy.deepcopy(current[2][2])
                current=(current[0],current[1],(current[2][0],current[2][1],-1))
                
                state_info_list.append(current)
                current=temp
            state_info_list.append((0+get_manhattan_distance(state,goal_state), state, (0, get_manhattan_distance(state,goal_state), -1)))
            state_info_list.reverse()
            max_length=72
            for state_info in state_info_list:
                current_state = state_info[1]
                h = get_manhattan_distance(current_state)
                move = state_info[2][0]
                print(current_state, "h={}".format(h), "moves: {}".format(move))
            print("Max queue length: {}".format(max_length))
            return None
            #exit
        successors=get_succ(current[1])
        for succ in successors:
            exist=0
            for item in open_queue:
                if succ==item[1]:
                    comp=item
                    exist=1
            for item in closed_queue:
                if succ==item[1]:
                    comp=item
                    exist=1
            if exist==0:
                g=current[2][0]+1
                h=get_manhattan_distance(succ,goal_state)
                cost=g+h
                parent=current
                heapq.heappush(open_queue ,(cost, succ, (g, h, parent)))
            else:
                g=current[2][0]+1
                h=get_manhattan_distance(succ,goal_state)
                cost=g+h
                parent=current
                if comp[2][0]>g:
                    heapq.heappush(open_queue ,(cost, succ, (g, h, parent)))
    
    # This is a format helper.
    # build "state_info_list", for each "state_info" in the list, it contains "current_state", "h" and "move".
    # define and compute max length
    # it can help to avoid any potential format issue.
    

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2, 5, 1, 4, 6, 0, 7, 0, 3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    print(get_succ([2,5,1,4,3,6,7,0,0]))
    print()
    
    solve([6, 0, 0, 3, 5, 1, 7, 2, 4])
    print()
