#include <bits/stdc++.h>
using namespace std;


vector<vector<int>> adj;
vector<int> vis;
bool dfs(int u){
  vis[u] = true;
  for(auto &v: adj[u])
    dfs(v);
}

int main(){
  int nodes = 7;
  int levels = 5;
  adj.assign(nodes,vector<int>());
  vis.assign(nodes,false);
  vector<tuple<int,int,int>> edges;

  vector<int> v[levels];
  v[0] = {0,1}; // agents
  v[1] = {2};
  v[2] = {3,4};
  v[3] = {5};
  v[4] = {6}; // source

  int prob = 100;
  srand(time(NULL));

  for(int i=0;i<levels;i++){
    for(auto &u: v[i]){
      prob = 80;
      for(int j=i + 1;j<levels;j++){
        prob-=20;
        for(auto &v: v[j]){
          int number = rand()%100;
          if(number < prob){
            int w = (j - i ) * (rand() % 10 + 1 ) ;
            edges.push_back({v,u,w});
            adj[v].push_back(u);
          }
        }
      }
    }
  }

  dfs(nodes - 1);
  bool ok = true;
  for(int i=0;i<v[0].size();i++){
    if(!vis[i]){
      ok = false;
      break;
    }
  }
  if(ok){
    cout << nodes << " " << edges.size() << "\n";
    for(auto &e: edges){
      cout << get<0>(e) << " " << get<1>(e) << " " << get<2>(e) << "\n";
    }
    for(int i=0;i<v[0].size();i++){
      cout << v[0][i] << " ";
    }

    cout << "\n" << v[levels - 1][0] << "\n";
  }
}
