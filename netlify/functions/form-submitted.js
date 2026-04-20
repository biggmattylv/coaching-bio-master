// CoachingBio Form Handler — Netlify Function
// Receives form submissions and returns card URL

exports.handler = async (event, context) => {
    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    };

    // Handle preflight
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    if (event.httpMethod !== 'POST') {
        return { statusCode: 405, headers, body: 'Method not allowed' };
    }

    try {
        const data = JSON.parse(event.body);
        const name = data.name || '';
        const email = data.email || '';

        if (!name || !email) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Name and email required' })
            };
        }

        // Create slug from name
        const slug = name.toLowerCase()
            .replace(/[^a-z0-9\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-')
            .trim();

        const cardUrl = `https://coachingbio.com/${slug}.html`;

        console.log('New submission:', JSON.stringify({ name, email, slug }));

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({
                success: true,
                message: 'Submission received',
                cardUrl: cardUrl,
                slug: slug
            })
        };

    } catch (error) {
        console.error('Error:', error.message);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ error: 'Processing failed: ' + error.message })
        };
    }
};
