#include<bits/stdc++.h>
#include <cctype>
using namespace std;

class Graph
{
    int V;    // No. of vertices
    list<int> *adjList;
    bool isCyclicUtil(int v, bool isVisited[], bool *rs);
public:
    Graph(int V);
    void addEdge(int v, int w);
    void printGraph(int v);
    bool isCyclic();
    void print(list<int>& mylist,int index);
};


void Graph::addEdge(int v, int w)
{
    adjList[v].push_back(w); // Add w to v’s list.
}

Graph::Graph(int V)
{
    this->V = V;
    adjList = new list<int>[V];
}

bool Graph::isCyclicUtil(int v, bool isVisited[], bool *recursiveStack)
{
    if(isVisited[v] == false)
    {
        // Mark the current node as isVisited and part of recursion stack
        isVisited[v] = true;
        recursiveStack[v] = true;

        // Recur for all the vertices from the list to this vertex
        list<int>::iterator i;
        for(i = adjList[v].begin(); i != adjList[v].end(); ++i)
        {
            if ( !isVisited[*i] && isCyclicUtil(*i, isVisited, recursiveStack) )
                return true;
            else if (recursiveStack[*i])
                return true;
        }

    }
    recursiveStack[v] = false;  // remove the vertex from recursion stack
    return false;
}

bool Graph::isCyclic()
{
    // Mark all the vertices as not isVisited and not part of recursion

    bool *isVisited = new bool[V];
    bool *recursiveStack = new bool[V];
    for(int i = 0; i < V; i++)
    {
        isVisited[i] = false;
        recursiveStack[i] = false;
    }

    // DFS trees
    for(int i = 0; i < V; i++)
        if ( !isVisited[i] && isCyclicUtil(i, isVisited, recursiveStack))
            return true;

    return false;
}


int main(){
    string input;
    string transactions[100];
    string str1 = "";
    string str2 = "";
    ifstream myFile("input.txt");

    int v = 4;
    Graph g(v);

    int i = 0;
    while (getline(myFile, input, ',')) {
        if(input[0]== ' ') input.erase(input.begin()+0);
        transactions[i++] = input;

    }

    int totalTransactions = i;


    for(int i = 0; i < totalTransactions-1; i++){
        string str1 = transactions[i];
        for(int j= i+1; j < totalTransactions; j++){
            string str2 = transactions[j];
            if(str1[3] == str2[3]){
                if((str1[1]!=str2[1]) && !(toupper(str1[0]) =='R' && toupper(str2[0])=='R')){
                    cout << str1 << "->" << str2 << endl;;
                    g.addEdge(str1[1]-48 , str2[1]-48);
                }
            }
        }
    }

     if(g.isCyclic())
        cout << "Cycle is found";
    else
        cout << "Cycle isn't found";
    return 0;

}


