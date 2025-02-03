export const USEFUL_SHAPES = [
  { name: 'circle', pictogram: 'circle' },
  { name: 'triangle', pictogram: 'change_history' },
  { name: 'square', pictogram: 'square' },
  { name: 'pentagon', pictogram: 'pentagon' },
  { name: 'star', pictogram: 'star' },
  { name: 'hexagon', pictogram: 'hexagon' },
  { name: 'heart', pictogram: 'favorite' },
  { name: 'cloud', pictogram: 'cloudy' },
];

export const UNKNOWN_SHAPE = 'help';

const SHAPES_MAP = new Map();

USEFUL_SHAPES.forEach(({ name, pictogram }) => {
  SHAPES_MAP.set(name, pictogram);
});

export function shapeToPicto(shape: string): string | undefined {
  return SHAPES_MAP.get(shape) || shape;
}
