#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

extern "C" {
    DLL_EXPORT void initialize_board();
    DLL_EXPORT bool is_valid_move(int row, int col, int player);
    DLL_EXPORT void make_move(int row, int col, int player);
    DLL_EXPORT void get_board(int* output);
    DLL_EXPORT bool has_valid_moves(int player);
}