"use client";
import { useParams, useRouter } from "next/navigation";

import { useState, useEffect } from "react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
const parse_result = (res: string): object[] => {
  let res_to_return = [
    {
      threat_level: "",
      type: "",
      description: "",
    },
  ];

  const splitted_res_result = res.split("\n");
  console.log(`splitted_res: ${splitted_res_result}`);
  for (let j = 0; j < splitted_res_result.length; j++) {
    res_to_return.push({
      threat_level: splitted_res_result[j].match(/\[[^\]]+\]/g)?.[0] || "",
      type: splitted_res_result[j].match(/\] (.*?):/)?.[1] || "",
      description: splitted_res_result[j].match(/: (.+)/)?.[1] || "",
    });
  }

  return res_to_return;
};

export default function ScanPage() {
  const [result, setResult] = useState<any[]>([]);
  const params = useParams();
  const { id } = params;
  const router = useRouter();

  useEffect(() => {
    fetch(`http://localhost:8000/scans/${id}`)
      .then((res) => res.json())
      .then((data) => {
        setResult(parse_result(String(data.result)));
      })
      .catch((err) => console.error(err));
  }, []);

  useEffect(() => {
    console.log(result);
  }, [result]);

  return (
    <div className="grid grid-rows-[20px_1fr_20px]flex items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)] ">
      <div>
        <Button onClick={() => router.push("/")}>Go Back</Button>
        <Table>
          <TableCaption>A list of scan results.</TableCaption>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[100px]">Threat Level</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Description</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {result
              .filter(
                (row) =>
                  row.threat_level !== "" ||
                  row.type !== "" ||
                  row.description !== ""
              )
              .map((row, idx) => (
                <TableRow key={idx}>
                  <TableCell className="font-medium">
                    {row.threat_level}
                  </TableCell>
                  <TableCell>{row.type}</TableCell>
                  <TableCell>{row.description}</TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
