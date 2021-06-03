'''
    This class provide a method of analyzing deepness of event-dependencies.
    Use case:
        SQL views that depend on other SQL views.
        Provide (list_of_normalized_dependencies) a list of tuples [(A,B),(A,C)] to represent that view A reads from views B and C
        and compute() will provide a "deepness", indicating the order those views shall be deployed
'''
class EventDependency:
    def __init__(self,list_of_normalized_dependencies):
        self.list_of_normalized_dependencies    =   list_of_normalized_dependencies
        unique_events                           =   list(set([x[0] for x in self.list_of_normalized_dependencies]))
        self.list_of_events                     =   sorted([(x,float('inf')) for x in unique_events],key=lambda tup: tup[0])
        self.max_event_name_length              =   len(max([x[0] for x in self.list_of_events], key=len))
    #-------------------------------------------------------------------------------------------------------------------
    def compute(self):
        #set level 0
        for current_event_normalized_dependencies in self.list_of_normalized_dependencies:
            event_name              =   current_event_normalized_dependencies[0]
            event_dependent_name    =   current_event_normalized_dependencies[1]
            if(event_dependent_name==None):
                self.list_of_events =   [(k,v) if (k!=event_name) else (k,0) for (k,v) in self.list_of_events]
        #set rest of levels
        finished            =   False
        iteration_number    =   -1
        while(not finished):
            iteration_number        +=  1
            #print(str(iteration_number))
            #check if we have finished
            remaining_event_names   =   [x[0] for x in self.list_of_events if x[1]==float('inf')]
            if(remaining_event_names==[]):
                finished    =   True
            for current_remaining_event_name in remaining_event_names:
                #print('\t'+current_remaining_event_name)
                dependant_events    =   [x[1] for x in self.list_of_normalized_dependencies if x[0]==current_remaining_event_name]
                max_deepness        =   0
                for current_remaining_current_dependency in dependant_events:
                    dependency_level    =   [x[1] for x in self.list_of_events if x[0]==current_remaining_current_dependency][0]
                    #print('\t\t'+current_remaining_current_dependency.ljust(self.max_event_name_length)+' - '+str(dependency_level))
                    if(dependency_level>max_deepness):
                        max_deepness    =   dependency_level
                if(max_deepness!=float('inf')):
                    self.list_of_events =   [(k, v) if (k != current_remaining_event_name) else (k,max_deepness+1) for (k, v) in self.list_of_events]
        return self.list_of_events
    #-------------------------------------------------------------------------------------------------------------------
    def print(self):
        for i in self.list_of_events:
            print(i[0].ljust(self.max_event_name_length,' ')+' - '+str(i[1]))

