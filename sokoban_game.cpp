#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MAXN = 20;

int n, m;
char a[MAXN][MAXN];
int sx, sy;
vector<pair<int, int>> boxes;

bool is_wall(int x, int y) {
    return a[x][y] == '#';
}

bool is_box(int x, int y) {
    return find(boxes.begin(), boxes.end(), make_pair(x, y)) != boxes.end();
}

bool is_goal(int x, int y) {
    return a[x][y] == 'G';
}

bool can_move(int x, int y) {
    if (is_wall(x, y)) {
        return false;
    }
    if (is_box(x, y)) {
        return !is_box(x + (x - sx), y + (y - sy)) && !is_wall(x + (x - sx), y + (y - sy));
    }
    return true;
}

bool is_win() {
    for (auto& box : boxes) {
        if (!is_goal(box.first, box.second)) {
            return false;
        }
    }
    return true;
}

void move_box(int x, int y) {
    for (int i = 0; i < boxes.size(); i++) {
        if (boxes[i].first == x && boxes[i].second == y) {
            boxes[i].first += x - sx;
            boxes[i].second += y - sy;
            return;
        }
    }
}

void move_player(int x, int y) {
    if (can_move(x, y)) {
        if (is_box(x, y)) {
            move_box(x, y);
        }
        sx = x;
        sy = y;
    }
}

void print_game() {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (sx == i && sy == j) {
                cout << "P";
            } else if (is_box(i, j)) {
                cout << "B";
            } else {
                cout << a[i][j];
            }
        }
        cout << endl;
    }
    cout << endl;
}

int main() {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> a[i][j];
            if (a[i][j] == 'P') {
                sx = i;
                sy = j;
            } else if (a[i][j] == 'B') {
                boxes.push_back(make_pair(i, j));
            }
        }
    }

    print_game();

    while (!is_win()) {
        char c;
        cin >> c;
        int nx = sx, ny = sy;
        if (c == 'U') {
            nx--;
        } else if (c == 'D') {
            nx++;
        } else if (c == 'L') {
            ny--;
        } else if (c == 'R') {
            ny++;
        }
        move_player(nx, ny);
        print_game();
    }

    cout << "You win!" << endl;

    return 0;
}