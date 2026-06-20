import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend-gateway:8000';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    
    const response = await fetch(`${BACKEND_URL}/api/upload`, {
      method: 'POST',
      body: formData,
      // Note: Do not manually set Content-Type for FormData, fetch handles the boundary automatically
    });
    
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Proxy error (upload):", error);
    return NextResponse.json({ error: "Failed to connect to backend" }, { status: 500 });
  }
}
