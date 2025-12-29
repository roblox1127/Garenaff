export async function onRequest(context) {
    const url = new URL(context.request.url);
    const username = url.searchParams.get('username');
    const corsHeaders = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,HEAD,POST,OPTIONS",
        "Content-Type": "application/json"
    };
    if (!username) return new Response(JSON.stringify({ completed: false }), { headers: corsHeaders });
    try {
        const isVerified = await context.env.BRAINROT_DB.get(username);
        return new Response(JSON.stringify({ completed: isVerified === "true" }), { headers: corsHeaders });
    } catch (err) {
        return new Response(JSON.stringify({ completed: false, error: err.message }), { headers: corsHeaders });
    }
}
