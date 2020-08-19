function sum(n) {
  if (n <= 0)
    return 0;
  let result = [];
  for (let i = 1; i <= n; i++) {
    result[i] = [];
    for (let j = 1; j <= i; j++) {
      if (j == 1 || i == 1) {
        result[i][j] = 1;
      } else {
        if (i == j) {
          result[i][j] = result[i][j - 1] + 1;
        } else if ((i - j) < j) {
          result[i][j] = result[i - j][i - j] + result[i][j - 1];
        } else {
          result[i][j] = result[i - j][j] + result[i][j - 1];
        }
      }
    }
  }
  return result[n][n];
}

// Examples
// Basic
// sum(1) // 1
 sum(2) // 2  -> 1+1 , 2
// sum(3) // 3 -> 1+1+1, 1+2, 3
// sum(4) // 5 -> 1+1+1+1, 1+1+2, 1+3, 2+2, 4
// sum(5) // 7 -> 1+1+1+1+1, 1+1+1+2, 1+1+3, 1+2+2, 1+4, 5, 2+3
// sum(10) // 42
// Explosive
// sum(50) // 204226
// sum(80) // 15796476
// sum(100) // 190569292