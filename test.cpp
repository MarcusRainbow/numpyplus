#include <cstdlib>
#include <cstdio>
#include <cassert>
#include <vector>
#include <exception>
#include <chrono>
using std::chrono::high_resolution_clock;
using std::chrono::duration_cast;
using std::chrono::milliseconds;

using std::vector;
using std::runtime_error;

int randint(int i)
{
    int r = std::rand();
    return r % i;
}

void reservoir_sampling_range(vector<int>& row, int low, int high)
{
    const int cols = row.size();
    for (int i = 0; i < cols; ++i)
        row[i] = i + low;

    for (int i = cols; i < high - low; ++i) {
        int j = randint(i);
        if (j < cols)
            row[j] = i + low;
    }
}

void reservoir_sampling_from(vector<int>& row, const vector<int>& source)
{
    int cols = row.size();
    int src_cols = source.size();

    for (int i = 0; i < cols; ++i)
        row[i] = source[i];

    for (int i = cols; i < src_cols; ++i) {
        int j = randint(i);
        if (j < cols)
            row[j] = source[i];
    }
}

void fisher_yates(vector<int>& row)
{
    for (int i = row.size() - 1; i > 0; --i) {
        int j = randint(i);
        int tmp = row[i];
        row[i] = row[j];
        row[j] = tmp;
    }
}

vector<vector<int>> randint_2d(int low, int high, int rows, int cols)
{
    int max_size = high - low;
    if (cols > max_size)
        throw runtime_error("randint_2d: cols is larger than high - low");

    vector<vector<int>> result;
    result.resize(rows);
    for (auto& row: result) {
        row.resize(cols);
        reservoir_sampling_range(row, low, high);
        fisher_yates(row);
    }
    return result;
}

vector<vector<int>> choice_2d(const vector<vector<int>>& a, int cols)
{
    int a_rows = a.size();
    int a_cols = a[0].size();

    vector<vector<int>> result;
    result.resize(a_rows);
    int i = 0;
    for (auto& row: result) {
        row.resize(cols);
        reservoir_sampling_from(row, a[i++]);
        fisher_yates(row);
    }
    return result;
}

void test_randint_2d()
{
    int max = 1000;
    int rows = 2000;
    int cols = 300;
    
    auto start = high_resolution_clock::now();
    auto result = randint_2d(0, max, rows, cols);
    auto elapsed = duration_cast<milliseconds>(high_resolution_clock::now() - start);
    
    assert(result.size() == rows);
    for (const auto& row: result) {
        assert(row.size() == cols);
        for (const auto element: row) {
            assert(element >= 0 && element < max);
        }
    }

    printf("test_random_2d succeeded in %lld ms\n", elapsed.count());
}

void test_choice_2d()
{
    int cols = 100;
    int rows = 2000;
    int a_cols = 300;
    int max = rows * a_cols;
    vector<vector<int>> array;
    array.resize(rows);
    int k = 0;
    for (auto& row: array) {
        row.resize(a_cols);
        for (auto& element: row) {
            element = k++;
        }
    }
    auto start = high_resolution_clock::now();
    auto result = choice_2d(array, cols);
    auto elapsed = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    
    assert(result.size() == rows);
    for (const auto& row: result) {
        assert(row.size() == cols);
        for (const auto element: row) {
            assert(element >= 0 && element < max);
        }
    }

    printf("test_choice_2d succeeded in %lld ms\n", elapsed.count());
}

int main(int argc, const char** argv)
{
    printf("hello world");
    try {
        test_randint_2d();
        test_choice_2d();
    } catch (const std::exception& e) {
        printf(e.what());
    }
}