#include <iostream>
#include <cstdio>
#include <stack>
#include <map>
#include <vector>
#include <string.h>
#include <set>

using namespace std;

#define MAX_BINXYZ 70
#define MAX_PART_NUM 10
#define MAX_ID_LEN 10
typedef pair<int, pair<int, int> > iii;
#define iii(a, b, c) make_pair(a, make_pair(b, c))

struct Part{
	char id[MAX_ID_LEN];
	int w, h, d;
	vector<int> orient;

	Part() {};
	Part(char *s, int a, int b, int c) {
		strcpy(id, s); w = a; h = b; d = c;

		set<iii> orientset;
		for (int j = 0; j < 6; j++) {
			iii o = get_orient(j);
			if (orientset.find(o) == orientset.end()) {
				orient.push_back(j);
				orientset.insert(o);
			}
		}
	}

	iii get_orient(int o) {
		int x, y, z;
		switch (o) {
			case 0:
				x = w; y = h; z = d;
				break;
			case 1:
				x = w; y = d; z = h;
				break;
			case 2:
				x = h; y = w; z = d;
				break;
			case 3:
				x = h; y = d; z = w;
				break;
			case 4:
				x = d; y = w; z = h;
				break;
			case 5:
				x = d; y = h; z = w;
				break;
		}
		return iii(x, y, z);
	}    
};

struct Result {
	char id[MAX_ID_LEN];
	int px, py, pz, x, y, z;
	Result() {};
	Result(char *s, int a, int b, int c, int d, int e, int f) {
		strcpy(id, s); px = a; py = b; pz = c; x = d, y = e; z = f;
	}
};

int binx, biny, binz;
int num_parts, num_links;
Part parts[MAX_PART_NUM];
stack<Result> tstack;
map<string, vector<string> > linkinfo;
int res_count;
int RESINDEX = 4;

void orient(int orientation, Part p, int &x, int &y, int &z) {
	switch (orientation) {
		case 0:
			x = p.w; y = p.h; z = p.d;
			break;
		case 1:
			x = p.w; y = p.d; z = p.h;
			break;
		case 2:
			x = p.h; y = p.w; z = p.d;
			break;
		case 3:
			x = p.h; y = p.d; z = p.w;
			break;
		case 4:
			x = p.d; y = p.w; z = p.h;
			break;
		case 5:
			x = p.d; y = p.h; z = p.w;
			break;
	}
}

int size_of_unfound(int arr[]) {
	int size = 0;
	for (int i = 0; i < num_parts; i++)
		if (!arr[i])
			size++;

	return size;
}

int pivot(int bin[][MAX_BINXYZ][MAX_BINXYZ], int &px, int &py, int &pz) {
	for (int i = 0; i < binx; i++)
		for (int j = 0; j < biny; j++)
			for (int k = 0; k < binz; k++)
				if (!bin[i][j][k]) {
					px = i; py = j; pz = k;
					return 1;
				}
	return 0;
}

int is_next_to(Result a, Result b) {
	int minx1 = a.px; int minx2 = b.px;
	int miny1 = a.py; int miny2 = b.py;
	int minz1 = a.pz; int minz2 = b.pz;

	int maxx1 = a.x + minx1; int maxx2 = b.x + minx2;
	int maxy1 = a.y + miny1; int maxy2 = b.y + miny2;
	int maxz1 = a.z + minz1; int maxz2 = b.z + minz2;

	return minx1 <= maxx2
    && minx2 <= maxx1
    && miny1 <= maxy2
    && miny2 <= maxy1
    && minz1 <= maxz2
    && minz2 <= maxz1;
}

int can_fit(int bin[][MAX_BINXYZ][MAX_BINXYZ], int px, int py, int pz, int x, int y, int z) {
	// must be within boundary
	if (px + x > binx || py + y > biny || pz + z > binz)
		return 0;

	// space must be empty
	for (int i = px; i < px + x; i++)
		for (int j = py; j < py + y; j++)
			for (int k = pz; k < pz + z; k++)
				if (bin[i][j][k])
					return 0;

	return 1;
}

int rec(int found[], int bin[][MAX_BINXYZ][MAX_BINXYZ]) {
	int px, py, pz;

	// find pivot
	int has_pivot = pivot(bin, px, py, pz);

	// we have reach the last part
	if (size_of_unfound(found) == 0)
		// no pivot means all space filled up, then we are done
		if (!has_pivot) {
			//printf("haha caught one!\n");
			stack<Result> resstack;
			map<string, Result> resmap;
			// extract result info
			while(!tstack.empty()) {
				Result r = tstack.top();
			    resstack.push(r);
			    resmap[r.id] = r;	
			    tstack.pop();
			}
			while(!resstack.empty()) {
			    tstack.push(resstack.top());
			    resstack.pop();
			}

			// check if satisfy link info
			int sat = 1;
			for (auto li : linkinfo) {
				Result a = resmap[li.first];
				vector<string> v = li.second;
				for (auto p : v) {
					Result b = resmap[p];
					if (!is_next_to(a, b)) {
						sat = 0; 
						break;
					}
				}
			}

			if (sat) {
				// print result
				res_count++;
				// if (res_count != RESINDEX)
				// 	return 0;

				cout << num_parts <<" 0" << endl;
				for (auto k : resmap) {
					Result item = k.second;
					printf("%s %f %f %f %f %f %f\n", item.id, item.px/(float)binx, item.py/(float)biny, item.pz/(float)binz, item.x/(float)binx, item.y/(float)biny, item.z/(float)binz);
					//printf("%s %d %d %d %d %d %d\n", item.id, item.px, item.py, item.pz, item.x, item.y, item.z);
				}
				cout<<endl;
				return 1;
			} else {
				//cout << "got result but not satified " << endl;
				return 0;
			}
		} else {
			return 0;
		}

	// cannot find space for next part
	if (!has_pivot)
		return 0;

	// for all remaining parts
	for (int i = 0; i < num_parts; i++) {
		if (!found[i]) {
			// for all orientations
			for (auto orientIndex : parts[i].orient) {
				int x, y, z;
				orient(orientIndex, parts[i], x, y, z);
				if (can_fit(bin, px, py, pz, x, y, z)) {
					// fit in 
					for (int i = px; i < px + x; i++)
						for (int j = py; j < py + y; j++)
							for (int k = pz; k < pz + z; k++)
								bin[i][j][k] = 1;
					found[i] = 1;
					//cout << "trying part " << i <<endl;
					// rec
					tstack.push(Result(parts[i].id, px, py, pz, x, y, z));
					int done = rec(found, bin);
					if (done) { 
						// if (res_count == RESINDEX)
						// 	return 1;
					}

					tstack.pop();
					// backtrack
					for (int i = px; i < px + x; i++)
						for (int j = py; j < py + y; j++)
							for (int k = pz; k < pz + z; k++)
								bin[i][j][k] = 0;
					found[i] = 0;
				}
			}
		}
	}

	return 0;
}

int main() {
	freopen("in4", "r", stdin);
	//freopen("out", "w", stdout);

	// read in
	scanf("%d %d %d", &binx, &biny, &binz);
	scanf("%d %d", &num_parts, &num_links);
	char s[MAX_ID_LEN];
	char t[MAX_ID_LEN];
	int w, h, d, n;
	for (int i = 0; i < num_parts; i++) {
		scanf("%s %d %d %d", &s, &w, &h, &d);
		parts[i] = Part(s, w, h, d);
	}

	for (int i = 0; i < num_links; i++) {
		scanf("%s %d", &s, &n);
		while (n--) {
			scanf("%s", &t);
			linkinfo[s].push_back(t);
		}
	}

	// for (auto k : linkinfo) {
	// 	vector<string> v = k.second;
	// 	for (auto j : v) {
	// 		cout << j << ' ';
	// 	}
	// 	cout << endl;
	// }

	// init
	int bin[MAX_BINXYZ][MAX_BINXYZ][MAX_BINXYZ];
	int found[MAX_PART_NUM];
	res_count = 0;
	//cout << size_of_unfound(found) << endl;
	rec(found, bin);

	cout << res_count << endl;
}

