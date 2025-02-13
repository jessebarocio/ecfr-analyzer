import { getAgency } from "@/lib/data";

export default async function AgencyPage({ params }: { params: { id: string } }) {

    const agency = await getAgency((await params).id);
    
    return <div>Agency Page - {agency.name}</div>;
}
