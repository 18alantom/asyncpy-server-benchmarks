import http from 'k6/http';
import { sleep } from 'k6';

const url = 'http://127.0.0.1:8000';

export const options = {
  vus: 10,
  duration: '60s',
};

export default function () {
  http.get(url);
  sleep(0.1);
  http.get(url + '/api');
  http.get(url);
}
