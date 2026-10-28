export interface CareerMatch {
  title: string;
  match: number;
}

export interface QuizResults {
  status: 'success';
  stream: string;
  optimal_vector: CareerMatch | null;
  evaluated_vectors: CareerMatch[];
  explanation: string;
  score_type: 'exploratory';
}

export function isQuizResults(value: unknown): value is QuizResults {
  if (typeof value !== 'object' || value === null) {
    return false;
  }

  const result = value as Record<string, unknown>;
  const isMatch = (match: unknown): match is CareerMatch => {
    if (typeof match !== 'object' || match === null) {
      return false;
    }

    const candidate = match as Record<string, unknown>;
    return (
      typeof candidate.title === 'string' &&
      typeof candidate.match === 'number' &&
      Number.isFinite(candidate.match) &&
      candidate.match >= 0 &&
      candidate.match <= 100
    );
  };

  return (
    result.status === 'success' &&
    typeof result.stream === 'string' &&
    (result.optimal_vector === null || isMatch(result.optimal_vector)) &&
    Array.isArray(result.evaluated_vectors) &&
    result.evaluated_vectors.length > 0 &&
    result.evaluated_vectors.every(isMatch) &&
    typeof result.explanation === 'string' &&
    result.score_type === 'exploratory'
  );
}
