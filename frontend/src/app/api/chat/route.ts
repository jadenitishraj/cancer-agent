import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://backend-gateway:8000';

export async function POST(request: Request) {
  try {
    const body = await request.text();
    
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body,
    });
    
    // For streaming responses, we pass the body directly back
    return new Response(response.body, {
      status: response.status,
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  } catch (error) {
    console.error("Proxy error (chat):", error);
    return NextResponse.json({ error: "Failed to connect to backend" }, { status: 500 });
  }
}
