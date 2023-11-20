/**
 * Not all promisified processes can run concurrently `setTimeout`
 * can run async on the event loop, i.e. if the event loop is single
 * threaded then multiple sleeps will take the same amount of time
 * as a single sleep.
 *
 * Looping over a `for` loop is not the same as `setTimeout` this
 * can be converted into a promise but in s single threaded event
 * loop the amount of time take is the sum of times take by each
 * loop call.
 */

const sleep = (d) => {
  return new Promise((r) => setTimeout(r, d));
};

const loop = (n) => {
  return new Promise((r) => {
    for (let i = 0; i < n; i++) {}
    r();
  });
};

const range = (n) => {
  return new Array(n).fill(null).map((_, i) => i);
};

async function testAsync(count, func, funcArg) {
  func ??= sleep;
  funcArg ??= 100;

  const label = `testAsync :: ${count} ✕ ${func.name}(${funcArg})`;

  console.time(label);
  const promises = range(count).map((_) => func(funcArg));
  await Promise.all(promises);
  console.timeEnd(label);
}

async function run() {
  await testAsync(1, sleep, 1000);
  await testAsync(20, sleep, 1000);

  await testAsync(1, loop, 500_000_000);
  await testAsync(20, loop, 500_000_000);
}

run();
