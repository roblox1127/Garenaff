export async function onRequest(context) {
    const API_KEY = "37019|udH6Fb4IC7cV942W6q6nIZl2qIsWR8Ep4YXVIygV68139ae4";
    const request = context.request;
    const url = new URL(request.url);
    const username = url.searchParams.get('username') || "Guest";
    const userCountry = request.cf?.country || 'US';
    const params = new URLSearchParams({ 
        ip: request.headers.get('CF-Connecting-IP') || '1.1.1.1',
        country_code: userCountry,
        user_agent: request.headers.get('User-Agent') || '',
        limit: '8',
        aff_sub5: "Garena"
    });
    try {
        const response = await fetch(`https://downloadlocked.com/api/v2/?${params.toString()}`, {
            headers: { "Authorization": `Bearer ${API_KEY}` }
        });
        const data = await response.json();
        const corsHeaders = { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" };
        if (data.success && data.offers) {
            const offers = data.offers.map(o => {
                let link = o.link || o.tracking_url;
                const sep = link.includes('?') ? '&' : '?';
                o.link = `${link}${sep}aff_sub4=${encodeURIComponent(username)}`;
                return o;
            });
            return new Response(JSON.stringify(offers), { headers: corsHeaders });
        }
        return new Response(JSON.stringify({ error: "No offers" }), { status: 400, headers: corsHeaders });
    } catch (e) {
        return new Response(JSON.stringify({ error: "Server Error" }), { status: 500, headers: corsHeaders });
    }
}
