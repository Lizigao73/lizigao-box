import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { SITE } from '../consts';

export async function GET(context) {
  const projects = await getCollection('projects');
  const sorted = projects.sort(
    (a, b) => b.data.startDate.getTime() - a.data.startDate.getTime()
  );

  return rss({
    title: SITE.name,
    description: SITE.description,
    site: context.site ?? SITE.url,
    items: sorted.map((project) => ({
      title: project.data.title,
      pubDate: project.data.startDate,
      description: project.data.summary,
      link: `/projects/${project.id}/`,
    })),
    customData: `<language>zh-CN</language>`,
  });
}
