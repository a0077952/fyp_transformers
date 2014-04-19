#include <iostream>
#include <algorithm>
#include <cstdio>
#include <vector>
#include <set>
#include <sstream>

using namespace std;

#define MAX_BINXYZ 70

typedef pair<int, pair<int, int> > iii;
#define iii(a, b, c) make_pair(a, make_pair(b, c))
#define itos(i) static_cast<ostringstream*>( &(ostringstream() << i) )->str()
#define NO_PIVOT iii(-1, -1, -1)

/////////////
class Part{
public:
	int count;
	int w, h, d;
	vector<int> orient;

	Part() {};
	
	Part(int a, int b, int c, int n) {
		// w h d are in increasing order
		w = a;
		h = b;
		d = c;
		count = n;

		// check different orientations
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

ostream& operator<<(ostream& os, const Part& rhs) {
	os << rhs.w << ' ' << rhs.h << ' ' << rhs.d;
	return os;
}

ostream& operator<<(ostream& os, const iii& i) {
	os << i.first << ' ' << i.second.first << ' ' << i.second.second;
	return os;
}

ostream& operator<<(ostream& os, const vector<int>& v) {
	for (int i = 0; i < v.size(); i++)
		os << v[i] << ' ';
	return os;
}
/////////////


int binx, biny, binz;
int num_parts;
int num_shapes;
vector<Part> partlist;
int bin[MAX_BINXYZ][MAX_BINXYZ][MAX_BINXYZ];
vector<iii> pivotlist;
int res_count = 0;
int try_c = 0;

iii get_pivot(int bin[][MAX_BINXYZ][MAX_BINXYZ]) {
	for (int i = 0; i < binx; i++)
		for (int j = 0; j < biny; j++)
			for (int k = 0; k < binz; k++)
				if (!bin[i][j][k]) {
					return iii(i, j, k);
				}
	return NO_PIVOT;
}

int fit_if_can(int (&bin)[MAX_BINXYZ][MAX_BINXYZ][MAX_BINXYZ], iii piv, iii pt) {
	// must be within boundary
	int px = piv.first;
	int py = piv.second.first;
	int pz = piv.second.second;
	int x = pt.first;
	int y = pt.second.first;
	int z = pt.second.second;

	if (px + x > binx || py + y > biny || pz + z > binz)
		return 0;

	// space must be empty
	for (int i = px; i < px + x; i++)
		for (int j = py; j < py + y; j++)
			for (int k = pz; k < pz + z; k++)
				if (bin[i][j][k]) {
					return 0;
				}

	// fit in
	for (int i = px; i < px + x; i++)
		for (int j = py; j < py + y; j++)
			for (int k = pz; k < pz + z; k++)
				bin[i][j][k] = 1;

	return 1;
}

void printbin(int bin[][MAX_BINXYZ][MAX_BINXYZ]) {
	for (int i = 0; i < binx; i++)
			for (int j = 0; j < biny; j++)
				for (int k = 0; k < binz; k++) {
					cout << iii(i, j, k) << ' ' << bin[i][j][k] <<endl;
				}
	cout <<endl;
}

// check if this combination can fit in
// print result on success
int checkfit(vector<int> perm, string orient) {
	pivotlist.clear();
	for (int i = 0; i < binx; i++)
		for (int j = 0; j < biny; j++)
			for (int k = 0; k < binz; k++)
				bin[i][j][k] = 0;

	//cout << "checking perm "<<perm<<" orient "<<orient <<endl;
	//printbin(bin);
	iii last_pivot;

	for (int index = 0; index < perm.size(); index++) {
		iii part_with_orient = partlist[perm[index]].get_orient((int)orient[index] - '0');
		iii pivot = get_pivot(bin);
		pivotlist.push_back(pivot);
		//printf("trying to fit %d, bin before fit\n", index);
		//printbin(bin);
		if (pivot != NO_PIVOT) {
			last_pivot = pivot;
			int can = fit_if_can(bin, pivot, part_with_orient);	
			//printf("trying to fit %d, bin after fit\n", index);
			//printbin(bin);
			if (!can) return 0;
		} else {
			return 0;
		}
	}

	// all parts has been fit into bin
	// check if there are empty spaces
	iii pp = get_pivot(bin);

	if (pp == NO_PIVOT) {
		// yeah!
		cout << "Result :" << res_count <<endl;
		for (int i = 0; i < pivotlist.size(); i++) {
			iii piv = pivotlist[i];
			iii part = partlist[perm[i]].get_orient((int)orient[i] - '0');
			cout << piv << ' ' << part << endl;
		}
		cout <<endl;
		return 1;
	} 

	return 0; 
}



// get orientation combinations for a permutation of parts
void comb(int index, vector<int> perm, string res){
	if (index == perm.size()) {
		//cout << "checking " << try_c << endl;
		try_c ++;
		if (checkfit(perm, res)) {
			res_count ++;
			//cout << "res_count" <<endl;
			//printbin(bin);
			
		}
		return;
	}

	Part p = partlist[perm[index]];
	for (auto e : p.orient) {
		comb(index + 1, perm, res + itos(e));
	}
}

void botup() {
	// gen permutations array
	vector<int> perm;
	for (int i = 0; i < num_shapes; i++) {
		Part p = partlist[i];
		for (int j = 0; j < p.count ; j++)
			perm.push_back(i);
	}

	// for each perm string
	// get all combination of orientations
	do {
		comb(0, perm, "");
	} while(next_permutation(perm.begin(), perm.end()));
}

void readin() {
	num_parts = 0;
	scanf("%d %d %d", &binx, &biny, &binz);
	scanf("%d", &num_shapes);

	int w, h, d, n;
	for (int i = 0; i < num_shapes; i++) {
		scanf("%d", &n);
		scanf("%d %d %d", &w, &h, &d);
		
		Part p(w, h, d, n);
		partlist.push_back(p);
		num_parts += n;
	}
}

int main() {
	freopen("in", "r", stdin);
	//freopen("out", "w", stdout);

	readin();
	botup();

	cout << res_count <<endl;
	cout << try_c <<endl;

}

