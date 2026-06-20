import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend-gateway:8000';

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/files`);
    const data = await response.json();
    
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Proxy error (files):", error);
    return NextResponse.json({ error: "Failed to connect to backend" }, { status: 500 });
  }
}
