// This file exports utility functions that can be used throughout the application.
export function formatDate(date, format) {
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  };
  return new Intl.DateTimeFormat('en-US', options).format(date);
}
export function calculateSum(numbers) {
  return numbers.reduce((acc, curr) => acc + curr, 0);
}
//# sourceMappingURL=helper.js.map
