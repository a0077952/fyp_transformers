#include <iostream>
#include <cstdio>
#include <stack>

using namespace std;

#define MAX_BINXYZ 70
#define MAX_PART_NUM 10

typedef pair<int, pair<int, int> > iii;
typedef pair<iii, iii> i6;
#define iii(a, b, c) make_pair(a, make_pair(b, c))
#define i6(a, b, c, d, e, f) make_pair(iii(a, b, c), iii(d, e, f))

struct Part{
	int w, h, d;
	Part() {};
	Part(int a, int b, int c) {
		w = a; h = b; d = c;
	}
};

int binx, biny, binz;
int num_parts;
Part parts[MAX_PART_NUM];
stack<i6> tstack;

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

	if (size_of_unfound(found) == 0)
		// no pivot means all space filled up, then we are done
		return !has_pivot;

	if (!has_pivot)
		return 0;

	// for all remaining parts
	for (int i = 0; i < num_parts; i++) {
		if (!found[i]) {
			// for all orientations
			for (int j = 0; j < 6; j++) {
				int x, y, z;
				orient(j, parts[i], x, y, z);
				if (can_fit(bin, px, py, pz, x, y, z)) {
					// fit in 
					for (int i = px; i < px + x; i++)
						for (int j = py; j < py + y; j++)
							for (int k = pz; k < pz + z; k++)
								bin[i][j][k] = 1;
					found[i] = 1;
					//cout << "trying part " << i <<endl;
					// rec
					tstack.push(i6(px, py, pz, x, y, z));
					int done = rec(found, bin);
					if (done) { 
						// print result
						//printf("%f %f %f %f %f %f\n", px/(float)binx, py/(float)biny, pz/(float)binz, x/(float)binx, y/(float)biny, z/(float)binz);
						//printf("%d %d %d %d %d %d\n", px, py, pz, x, y, z);
						//return 1;
						printf("haha caught one!\n");
						stack<i6> temp;
						while(!tstack.empty()) {
					        temp.push(tstack.top());
					        tstack.pop();
					    }

					    while(!temp.empty()) {
					    	i6 item = temp.top();
					        tstack.push(item);
					    	printf("%d %d %d %d %d %d\n", item.first.first, item.first.second.first, item.first.second.second, item.second.first, item.second.second.first, item.second.second.second);
					        temp.pop();
					    }
					    int j=0;
					    for (int i=0; i< 200; i++)
					    	j++;
					    cout <<endl;

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

void botup() {
	// all permutations
}

int main() {
	freopen("in4", "r", stdin);
	//freopen("out", "w", stdout);

	// read in
	scanf("%d %d %d", &binx, &biny, &binz);
	scanf("%d", &num_parts);
	int w, h, d;
	for (int i = 0; i < num_parts; i++) {
		scanf("%d %d %d", &w, &h, &d);
		parts[i] = Part(w, h, d);
	}

	// init bin
	int bin[MAX_BINXYZ][MAX_BINXYZ][MAX_BINXYZ];
	int found[MAX_PART_NUM];

	//cout << size_of_unfound(found) << endl;
	rec(found, bin);

}

