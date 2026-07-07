import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

type Point = { step: number; epoch: number; loss: number }

export default function LossChart({ data }: { data: Point[] }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="step" label={{ value: 'Étape', position: 'insideBottom', offset: -5 }} />
        <YAxis label={{ value: 'Loss', angle: -90, position: 'insideLeft' }} />
        <Tooltip />
        <Line type="monotone" dataKey="loss" stroke="#4f7cff" dot={false} strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  )
}
