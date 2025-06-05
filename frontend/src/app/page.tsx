"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Loader2 } from "lucide-react";
import { useState, useEffect } from "react";
import Link from "next/link";

const start_scan = async (url: string) => {
  const response = await fetch("http://localhost:8000/scans/start", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url: url,
      status: "pending",
      result: "",
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
};

export default function Home() {
  const [result, setResult] = useState<any[]>([]);
  const [inputUrl, setInputUrl] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const refreshScans = async () => {
    const res = await fetch("http://localhost:8000/scans/all");
    const data = await res.json();
    setResult(data);
  };

  useEffect(() => {
    refreshScans().catch(console.error);
  }, []);

  const handleScan = async () => {
    if (!inputUrl) return;
    setLoading(true);
    try {
      await start_scan(inputUrl);
      await refreshScans();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <div></div>
      <Card className="w-3/5 h-full p-15">
        <CardHeader>
          <CardTitle>
            <h1>Vulnerability Scanner</h1>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex w-3/5 justify-around">
            <Input
              className="mr-5"
              placeholder="https://example.com"
              value={inputUrl}
              onChange={(e) => setInputUrl(e.target.value)}
              disabled={loading}
            />
            <Button type="button" onClick={handleScan} disabled={loading}>
              {loading ? (
                <div className="flex items-center">
                  <Loader2 className="animate-spin mr-2 w-4 h-4" />
                  Scanning...
                </div>
              ) : (
                "Start scan"
              )}
            </Button>
          </div>
        </CardContent>
        <CardFooter>
          <Table>
            <TableCaption>Your scans</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[100px]">ID</TableHead>
                <TableHead>Url</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {result.map((scan, i) => (
                <TableRow key={scan.id ?? i}>
                  <TableCell className="font-medium">
                    <Link href={`/scan/${scan.id}`}>{scan.id ?? "N/A"}</Link>
                  </TableCell>
                  <TableCell>
                    <Link href={`/scan/${scan.id}`}>{scan.url ?? "N/A"}</Link>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardFooter>
      </Card>
      <div></div>
    </div>
  );
}
