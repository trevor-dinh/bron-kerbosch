DEBUG = False


class Trace_Calls: 
#Credit goes to Richard Pattis for his Illustrate_Recursive class.
#Source:https://www.ics.uci.edu/~pattis/ICS-33/lectures/decoratorspackages.txt
    def __init__(self,f):
        self.f = f
        self.calls = 0
        self.trace = False
        self.record = []


    def illustrate(self,*args,**kargs):
        
        self.indent = 0
        self.trace = True
        answer = self.__call__(*args,**kargs)
        self.trace = False
        return answer
    
    # def __call__(self,*args,**kargs):  # bundle arbitrary arguments to this call
    #     self.calls += 1
    #     return self.f(*args,**kargs)  # unbundle arbitrary arguments to call f

    def display_records(self):
        return self.record

    def __call__(self,*args,**kargs):

        if self.trace:
            if self.indent == 0:
                print('Starting recursive illustration'+30*'-')
            print (self.indent*"."+"calling", self.f.__name__+str(args)+str(kargs))
            self.indent += 2
        self.calls += 1
        answer = self.f(*args,**kargs)
        if answer != None:
            self.record.append(answer)
        if self.trace:
            self.indent -= 2
            print (self.indent*"."+self.f.__name__+str(args)+str(kargs)+" returns", answer)
            if self.indent == 0:
                print('Ending recursive illustration'+30*'-')
        return answer
    def called(self):
        return self.calls

    def get_recursive_calls(self):
        return self.calls - 1
    
    def reset(self):
        self.calls = 0
        self.record = []


def trace(f): #Visualize recursive calls
    trace.recursive_calls = 0
    trace.depth = 0


    def _f(*args, **kwargs):


        print("  " * trace.depth, ">", f.__name__, args, kwargs)
        if trace.depth >= 1:
            trace.recursive_calls += 1
        trace.depth += 1
        res = f(*args, **kwargs)
        trace.depth -= 1
        print("  " * trace.depth, "<", res)
        print("recursive calls so far: {}".format(trace.recursive_calls))
        return res
    return _f
@Trace_Calls
def bron_kerbosch(R, P, X, graph, find_pivot=False):
    if len(P) == 0:
        if len(X) == 0:
            
            return R
    else:
        frontier = set(P)
        if find_pivot:
            #print("found_pivot")
            u = find_max_pivot(graph, P, X)
            #print(set(P), set(graph[u]))
            frontier = set(P) - set(graph[u])
        for v in frontier:
            # if DEBUG:
            #     print("BronKerbosch({}, {}, {})".format(
            #         R.union({v}),
            #         P.intersection(set(N(v,graph))),
            #         X.intersection(set(N(v,graph)))
            #         ))
            bron_kerbosch(
                R.union({v}),
                P.intersection(set(graph[v])),
                X.intersection(set(graph[v])),
                graph,
                find_pivot
             )

            P.remove(v)

            X = X.union({v})

def find_max_pivot(graph, P, X):
    nodes = list(P.union(X))
    u = nodes[0]
    max_intersection = len(set(graph[nodes[0]]).intersection(P))
    for n in nodes:
        if len(set(graph[n]).intersection(P)) > max_intersection:
            u = n
            max_intersection = len(set(graph[n]).intersection(P))

    return u


def bk_initial_call(graph, pivot=False, visualize=False):
    f = bron_kerbosch
    #print(f)

    if visualize:
        f.illustrate(set(), set(graph.keys()), set(), graph, pivot)
    else:
        f(set(), set(graph.keys()), set(), graph, pivot)
    print(f.get_recursive_calls())
    print(f.display_records())
    f.reset()

def N(v, g):
    # for i, n_v in enumerate(g[v]):
    #     print(i, n_v)
    #print("{}->{}".format(v,[n_v for i, n_v in enumerate(g[v]) if n_v]))

    return [n_v for i, n_v in enumerate(g[v]) if n_v]
test_graph = {
    1 : [2,5],
    2 : [1,3,5],
    3 : [2,4],
    4 : [3,5,6],
    5 : [1,2,4],
    6 : [4]
}
frucht = {
    1 : [12,2,3],
    2 : [1,3,11],
    3 : [1,2, 4],
    4 : [3,5,6],
    5 : [4,6,10],
    6 : [4,5,7],
    7 : [6,8,9],
    8 : [7,9,10],
    9 : [7,8,12],
    10 : [5,8,11],
    11 : [2,10,12],
    12 : [1,9,11]
}

complete_graph_4 = {
    1 : [2,3,4],
    2 : [1,3,4],
    3 : [1,2,4],
    4 : [1,2,3]
}


if __name__ == '__main__':
    #print(set([1,2,3,4]))
    # print(set(test_graph.keys()))
    # init_bkb(test_graph)
    #init_bkb(frucht, pivot=True)
    bk_initial_call(complete_graph_4)
    print("Pivot")

    bk_initial_call(complete_graph_4, pivot=True, visualize=True)