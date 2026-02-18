interface SparklineProps {
  data: number[];
  width?: number;
  height?: number;
}

const Sparkline = ({ data, width = 80, height = 24 }: SparklineProps) => {
  if (!data.length) return null;

  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;

  const points = data
    .map((val, i) => {
      const x = (i / (data.length - 1)) * width;
      const y = height - ((val - min) / range) * height;
      return `${x},${y}`;
    })
    .join(" ");

  const isUp = data[data.length - 1] >= data[0];

  return (
    <svg width={width} height={height} className="inline-block">
      <polyline
        points={points}
        fill="none"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={isUp ? "sparkline-up" : "sparkline-down"}
      />
    </svg>
  );
};

export default Sparkline;
