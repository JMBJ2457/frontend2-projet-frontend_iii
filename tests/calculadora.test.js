import { expect, test } from 'vitest';
import { sumar } from '../src/calculadora';

test('Debe sumar 2 + 3 y retornar 5', () => {
  expect(sumar(2, 3)).toBe(5);
});
