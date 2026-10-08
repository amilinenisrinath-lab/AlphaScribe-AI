"use client";

import React, { useState } from "react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import { BarChart3, Image as ImageIcon } from "lucide-react";
import { API_BASE_URL } from "@/lib/api";

interface FinancialChartsProps {
  ticker: string;
  chartUrl?: string;
}

const mockChartData = [
  { period: "2020", revenue: 274.5, margin: 24.1 },
  { period: "2021", revenue: 365.8, margin: 25.8 },
  { period: "2022", revenue: 394.3, margin: 25.3 },
  { period: "2023", revenue: 383.3, margin: 25.3 },
  { period: "2024", revenue: 391.0, margin: 26.2 },
];

export const FinancialCharts: React.FC<FinancialChartsProps> = ({
  ticker,
  chartUrl,
}) => {
  const [viewMode, setViewMode] = useState<"interactive" | "r_image">("interactive");

  return (
    <div className="bg-gray-950 border border-gray-800 rounded-xl p-4 my-4 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-blue-400" />
          <h4 className="text-xs font-bold text-gray-200 uppercase tracking-wider">
            {ticker} Financial Analytics Engine
          </h4>
        </div>

        {/* View Toggle */}
        <div className="flex items-center bg-gray-900 border border-gray-800 rounded-lg p-0.5 text-xs">
          <button
            onClick={() => setViewMode("interactive")}
            className={`px-2.5 py-1 rounded-md transition font-medium ${
              viewMode === "interactive"
                ? "bg-blue-600 text-white shadow-sm"
                : "text-gray-400 hover:text-white"
            }`}
          >
            Interactive Recharts
          </button>
          <button
            onClick={() => setViewMode("r_image")}
            className={`px-2.5 py-1 rounded-md transition font-medium flex items-center gap-1 ${
              viewMode === "r_image"
                ? "bg-purple-600 text-white shadow-sm"
                : "text-gray-400 hover:text-white"
            }`}
          >
            <ImageIcon className="w-3 h-3" />
            R ggplot2 Output
          </button>
        </div>
      </div>

      {viewMode === "interactive" ? (
        <div className="h-60 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={mockChartData}>
              <defs>
                <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis dataKey="period" stroke="#64748b" fontSize={11} />
              <YAxis
                stroke="#64748b"
                fontSize={11}
                tickFormatter={(val) => `$${val}B`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  borderColor: "#334155",
                  borderRadius: "8px",
                  fontSize: "12px",
                }}
              />
              <Area
                type="monotone"
                dataKey="revenue"
                stroke="#3b82f6"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorRev)"
                name="Total Revenue ($B)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center p-4 bg-gray-900 rounded-lg border border-gray-800">
          {chartUrl ? (
            <img
              src={`${API_BASE_URL}${chartUrl}`}
              alt={`${ticker} ggplot2 chart`}
              className="rounded shadow-md max-h-72 object-contain"
            />
          ) : (
            <div className="text-xs text-gray-500 py-10">
              Run the analysis to generate the R ggplot2 chart asset.
            </div>
          )}
          <span className="text-[10px] text-gray-400 mt-2">
            Generated via backend R script bridge with 300 DPI resolution.
          </span>
        </div>
      )}
    </div>
  );
};
